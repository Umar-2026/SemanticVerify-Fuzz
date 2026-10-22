#include <algorithm>
#include <cctype>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <deque>
#include <map>
#include <memory>
#include <optional>
#include <set>
#include <sstream>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

#include "clang/AST/AST.h"
#include "clang/AST/ASTContext.h"
#include "clang/AST/ASTTypeTraits.h"
#include "clang/AST/ParentMapContext.h"
#include "clang/AST/RecursiveASTVisitor.h"
#include "clang/Analysis/CFG.h"
#include "clang/Basic/SourceManager.h"
#include "clang/Frontend/CompilerInstance.h"
#include "clang/Frontend/FrontendActions.h"
#include "clang/Lex/Lexer.h"
#include "clang/Tooling/CommonOptionsParser.h"
#include "clang/Tooling/Tooling.h"
#include "llvm/ADT/StringRef.h"
#include "llvm/Support/CommandLine.h"
#include "llvm/Support/Error.h"
#include "llvm/Support/JSON.h"
#include "llvm/Support/MemoryBuffer.h"
#include "llvm/Support/Path.h"
#include "llvm/Support/raw_ostream.h"

using namespace clang;
using namespace clang::tooling;

namespace {

static llvm::cl::OptionCategory SVFCategory("semanticverify-clang-cfg-v1");
static llvm::cl::opt<std::string> SpecPath(
    "spec", llvm::cl::desc("Frozen canonical zlib protocol specification"),
    llvm::cl::value_desc("path"), llvm::cl::Required, llvm::cl::cat(SVFCategory));
static llvm::cl::opt<std::string> ContractPath(
    "contract", llvm::cl::desc("Frozen protocol obligation contract"),
    llvm::cl::value_desc("path"), llvm::cl::Required, llvm::cl::cat(SVFCategory));
static llvm::cl::opt<unsigned> StateCap(
    "state-cap", llvm::cl::desc("Development abstract-state cap per CFG block"),
    llvm::cl::init(64), llvm::cl::cat(SVFCategory));

static std::string trimCopy(std::string S) {
  auto NotSpace = [](unsigned char C) { return !std::isspace(C); };
  auto B = std::find_if(S.begin(), S.end(), NotSpace);
  auto E = std::find_if(S.rbegin(), S.rend(), NotSpace).base();
  if (B >= E) return "";
  return std::string(B, E);
}

static std::vector<std::string> splitByLiteral(const std::string &S,
                                               const std::string &Sep) {
  std::vector<std::string> Out;
  size_t Pos = 0;
  while (Pos <= S.size()) {
    size_t N = S.find(Sep, Pos);
    if (N == std::string::npos) {
      Out.push_back(trimCopy(S.substr(Pos)));
      break;
    }
    Out.push_back(trimCopy(S.substr(Pos, N - Pos)));
    Pos = N + Sep.size();
  }
  return Out;
}

static bool isIdentifier(const std::string &S) {
  if (S.empty()) return false;
  if (!(std::isalpha(static_cast<unsigned char>(S[0])) || S[0] == '_'))
    return false;
  for (char C : S) {
    if (!(std::isalnum(static_cast<unsigned char>(C)) || C == '_'))
      return false;
  }
  return true;
}

static std::string jsonEscape(llvm::StringRef S) {
  std::string O;
  O.reserve(S.size() + 16);
  static const char Hex[] = "0123456789abcdef";
  for (unsigned char C : S) {
    switch (C) {
      case '"': O += "\\\""; break;
      case '\\': O += "\\\\"; break;
      case '\b': O += "\\b"; break;
      case '\f': O += "\\f"; break;
      case '\n': O += "\\n"; break;
      case '\r': O += "\\r"; break;
      case '\t': O += "\\t"; break;
      default:
        if (C < 0x20) {
          O += "\\u00";
          O += Hex[(C >> 4) & 0x0f];
          O += Hex[C & 0x0f];
        } else {
          O.push_back(static_cast<char>(C));
        }
    }
  }
  return O;
}

static std::string jsonString(llvm::StringRef S) {
  return "\"" + jsonEscape(S) + "\"";
}

struct SourcePoint {
  std::string file;
  unsigned line = 0;
  unsigned column = 0;
  unsigned offset = 0;
};

struct TransitionSpec {
  std::string id;
  std::string eventId;
  std::vector<std::string> fromStates;
  std::vector<std::string> toStates;
  std::string ownershipEffect;
  std::string returnPredicate;
};

struct RuleSpec {
  std::string id;
  std::string defectCategory;
  std::string resourceKind;
  std::string trigger;
  std::string precondition;
  std::string returnPredicate;
  std::string cleanupResponsibility;
  std::vector<std::string> permittedTransitions;
};

enum class EventSemanticKind {
  Init,
  Use,
  OrderedConfiguration,
  StateTransition,
  End,
  Unsupported
};

struct EventSpec {
  std::string id;
  std::string kind;
  std::string condition;
  std::vector<std::string> symbols;
  EventSemanticKind semanticKind = EventSemanticKind::Unsupported;
  std::string family;
  std::string successConstant;
  std::string successState;
  std::string failureState;
  std::string releaseState;
  std::string prerequisiteResourceRole;
};

struct SpecModel {
  std::string schemaVersion;
  std::string specificationId;
  std::string libraryRevision;
  std::string declaredContentSha256;
  std::string initialState;
  std::set<std::string> states;
  std::vector<EventSpec> events;
  std::vector<TransitionSpec> transitions;
  std::vector<RuleSpec> rules;
  std::map<std::string, size_t> symbolToEvent;
  std::set<std::string> limitationCodes;

  const EventSpec *eventById(llvm::StringRef Id) const {
    for (const auto &E : events) if (E.id == Id) return &E;
    return nullptr;
  }

  const EventSpec *eventBySymbol(llvm::StringRef Symbol) const {
    auto It = symbolToEvent.find(Symbol.str());
    if (It == symbolToEvent.end()) return nullptr;
    return &events[It->second];
  }

  std::vector<const TransitionSpec *> transitionsForEvent(llvm::StringRef Id) const {
    std::vector<const TransitionSpec *> Out;
    for (const auto &T : transitions) if (T.eventId == Id) Out.push_back(&T);
    return Out;
  }

  std::vector<const TransitionSpec *> transitionsFrom(llvm::StringRef EventId,
                                                       llvm::StringRef State) const {
    std::vector<const TransitionSpec *> Out;
    for (const auto &T : transitions) {
      if (T.eventId != EventId) continue;
      if (std::find(T.fromStates.begin(), T.fromStates.end(), State.str()) != T.fromStates.end())
        Out.push_back(&T);
    }
    return Out;
  }

  std::string ruleFor(const std::string &Category, const std::string &Family,
                      bool FunctionExitOnly = false) const {
    for (const auto &R : rules) {
      if (R.defectCategory != Category) continue;
      if (R.resourceKind.find(Family) == std::string::npos) continue;
      if (FunctionExitOnly && R.trigger.find("FUNCTION_EXIT") == std::string::npos) continue;
      return R.id;
    }
    return "";
  }

  std::string ruleForCategory(const std::string &Category) const {
    for (const auto &R : rules) {
      if (R.defectCategory == Category) return R.id;
    }
    return "";
  }

  std::string ruleForEvent(const std::string &Category,
                           const EventSpec &Event) const {
    auto IsIdentifierCharacter = [](char C) {
      return (C >= 'a' && C <= 'z') ||
             (C >= 'A' && C <= 'Z') ||
             (C >= '0' && C <= '9') ||
             C == '_';
    };

    for (const auto &R : rules) {
      if (R.defectCategory != Category) continue;
      for (const auto &Symbol : Event.symbols) {
        if (Symbol.empty()) continue;
        size_t SearchFrom = 0;
        while (true) {
          size_t Pos = R.trigger.find(Symbol, SearchFrom);
          if (Pos == std::string::npos) break;
          size_t SymbolEnd = Pos + Symbol.size();
          bool LeftBoundary =
              Pos == 0 || !IsIdentifierCharacter(R.trigger[Pos - 1]);
          bool RightBoundary =
              SymbolEnd == R.trigger.size() ||
              !IsIdentifierCharacter(R.trigger[SymbolEnd]);
          if (LeftBoundary && RightBoundary) return R.id;
          SearchFrom = Pos + 1;
        }
      }
    }
    return "";
  }


  std::string ruleForAcquisition(
      const std::string &Category,
      const std::string &Family,
      const std::string &AcquisitionEvent,
      bool FunctionExitOnly = false) const {
    for (const auto &T : transitions) {
      if (T.eventId != AcquisitionEvent ||
          T.ownershipEffect != "ACQUIRE")
        continue;
      for (const auto &R : rules) {
        if (R.defectCategory != Category) continue;
        if (FunctionExitOnly &&
            R.trigger.find("FUNCTION_EXIT") ==
                std::string::npos)
          continue;
        if (std::find(
                R.permittedTransitions.begin(),
                R.permittedTransitions.end(),
                T.id) !=
            R.permittedTransitions.end())
          return R.id;
      }
    }
    return ruleFor(Category, Family, FunctionExitOnly);
  }

  std::string conditionedCleanupRule() const {
    for (const auto &R : rules) {
      if (R.defectCategory == "D8") return R.id;
    }
    return "";
  }
};

static std::string requireString(const llvm::json::Object &O, llvm::StringRef Key) {
  auto V = O.getString(Key);
  if (!V) {
    llvm::errs() << "SPEC_ERROR: missing string field " << Key << "\n";
    std::exit(20);
  }
  return V->str();
}

static std::vector<std::string> stringArray(const llvm::json::Object &O,
                                            llvm::StringRef Key) {
  std::vector<std::string> Out;
  auto *A = O.getArray(Key);
  if (!A) return Out;
  for (const auto &V : *A) {
    auto S = V.getAsString();
    if (!S) {
      llvm::errs() << "SPEC_ERROR: non-string item in " << Key << "\n";
      std::exit(21);
    }
    Out.push_back(S->str());
  }
  return Out;
}

static std::string familyFromStates(const TransitionSpec &T) {
  auto Check = [](const std::string &S) -> std::string {
    if (S.find("DEFLATE") != std::string::npos) return "deflate";
    if (S.find("INFLATE") != std::string::npos) return "inflate";
    return "";
  };
  for (const auto &S : T.fromStates) {
    std::string F = Check(S); if (!F.empty()) return F;
  }
  for (const auto &S : T.toStates) {
    std::string F = Check(S); if (!F.empty()) return F;
  }
  return "";
}

static std::string parseSimpleReturnConstant(
    const std::string &Predicate,
    const std::string &Operator) {
  std::string Needle = "return " + Operator + " ";
  std::string P = trimCopy(Predicate);
  size_t Pos = P.find(Needle);
  while (Pos != std::string::npos) {
    bool AtPredicateStart = Pos == 0;
    bool AfterConjunction =
        Pos >= 5 && P.compare(Pos - 5, 5, " and ") == 0;
    if (AtPredicateStart || AfterConjunction) {
      std::string Tail =
          trimCopy(P.substr(Pos + Needle.size()));
      size_t Space = Tail.find_first_of(" ;&|");
      if (Space != std::string::npos)
        Tail = Tail.substr(0, Space);
      if (isIdentifier(Tail)) return Tail;
    }
    Pos = P.find(Needle, Pos + 1);
  }
  return "";
}

static std::string parseValidResourcePrerequisite(
    const std::string &Predicate) {
  std::string P = trimCopy(Predicate);
  const std::string Marker = " valid and return == ";
  size_t Pos = P.find(Marker);
  if (Pos == std::string::npos) return "";
  std::string Role = trimCopy(P.substr(0, Pos));
  return isIdentifier(Role) ? Role : "";
}

static std::vector<std::string> parseEventSymbols(const std::string &Condition) {
  std::string Head = Condition.substr(0, Condition.find(';'));
  std::vector<std::string> Out;
  for (const auto &Part : splitByLiteral(Head, " or ")) {
    if (isIdentifier(Part)) Out.push_back(Part);
  }
  return Out;
}

static SpecModel loadSpecAndContract(const std::string &SpecFile,
                                     const std::string &ContractFile) {
  SpecModel M;
  auto SpecBuf = llvm::MemoryBuffer::getFile(SpecFile);
  if (!SpecBuf) {
    llvm::errs() << "SPEC_ERROR: cannot read " << SpecFile << "\n";
    std::exit(22);
  }
  auto Parsed = llvm::json::parse((*SpecBuf)->getBuffer());
  if (!Parsed) {
    llvm::errs() << "SPEC_ERROR: invalid JSON: " << llvm::toString(Parsed.takeError()) << "\n";
    std::exit(23);
  }
  auto *Root = Parsed->getAsObject();
  if (!Root) {
    llvm::errs() << "SPEC_ERROR: root is not an object\n";
    std::exit(24);
  }
  M.schemaVersion = requireString(*Root, "schema_version");
  M.specificationId = requireString(*Root, "specification_id");
  M.libraryRevision = requireString(*Root, "library_revision");
  M.declaredContentSha256 = requireString(*Root, "content_sha256");
  M.initialState = requireString(*Root, "initial_state");
  for (const auto &S : stringArray(*Root, "states")) M.states.insert(S);

  auto *Events = Root->getArray("events");
  if (!Events) {
    llvm::errs() << "SPEC_ERROR: events missing\n";
    std::exit(25);
  }
  for (const auto &V : *Events) {
    auto *O = V.getAsObject();
    if (!O) { llvm::errs() << "SPEC_ERROR: event not object\n"; std::exit(26); }
    EventSpec E;
    E.id = requireString(*O, "event_id");
    E.kind = requireString(*O, "event_kind");
    E.condition = requireString(*O, "symbol_or_condition");
    if (E.kind == "API_CALL") E.symbols = parseEventSymbols(E.condition);
    M.events.push_back(std::move(E));
  }

  auto *Transitions = Root->getArray("transitions");
  if (!Transitions) { llvm::errs() << "SPEC_ERROR: transitions missing\n"; std::exit(27); }
  for (const auto &V : *Transitions) {
    auto *O = V.getAsObject();
    if (!O) { llvm::errs() << "SPEC_ERROR: transition not object\n"; std::exit(28); }
    TransitionSpec T;
    T.id = requireString(*O, "transition_id");
    T.eventId = requireString(*O, "event_id");
    T.fromStates = stringArray(*O, "from_states");
    T.toStates = stringArray(*O, "to_states");
    T.ownershipEffect = requireString(*O, "ownership_effect");
    if (auto P = O->getString("return_predicate")) T.returnPredicate = P->str();
    M.transitions.push_back(std::move(T));
  }

  auto *Obligations = Root->getArray("obligations");
  if (!Obligations) { llvm::errs() << "SPEC_ERROR: obligations missing\n"; std::exit(29); }
  for (const auto &V : *Obligations) {
    auto *O = V.getAsObject();
    if (!O) { llvm::errs() << "SPEC_ERROR: obligation not object\n"; std::exit(30); }
    RuleSpec R;
    R.id = requireString(*O, "rule_id");
    R.defectCategory = requireString(*O, "defect_category");
    R.resourceKind = requireString(*O, "resource_kind");
    R.trigger = requireString(*O, "triggering_event_or_function_exit");
    R.precondition = requireString(*O, "required_pre_state_or_exit_condition");
    if (auto P = O->getString("return_predicate")) R.returnPredicate = P->str();
    R.cleanupResponsibility = requireString(*O, "cleanup_responsibility");
    R.permittedTransitions =
        stringArray(*O, "permitted_transitions");
    M.rules.push_back(std::move(R));
  }

  for (size_t I = 0; I < M.events.size(); ++I) {
    auto &E = M.events[I];
    for (const auto &S : E.symbols) {
      if (M.symbolToEvent.count(S)) {
        llvm::errs() << "SPEC_ERROR: duplicate API symbol " << S << "\n";
        std::exit(31);
      }
      M.symbolToEvent[S] = I;
    }

    bool HasAcquire = false, HasRelease = false;
    bool AllOwnershipPreserving = true;
    bool AllStatePreserving = true;
    size_t TransitionCount = 0;
    std::set<std::string> EqConstants, NeConstants;
    for (const auto &T : M.transitions) {
      if (T.eventId != E.id) continue;
      ++TransitionCount;
      if (T.ownershipEffect != "NONE")
        AllOwnershipPreserving = false;
      if (T.fromStates != T.toStates)
        AllStatePreserving = false;
      if (E.family.empty()) E.family = familyFromStates(T);
      std::string EqC = parseSimpleReturnConstant(T.returnPredicate, "==");
      std::string NeC = parseSimpleReturnConstant(T.returnPredicate, "!=");
      std::string RequiredRole =
          parseValidResourcePrerequisite(T.returnPredicate);
      if (!RequiredRole.empty()) {
        if (!E.prerequisiteResourceRole.empty() &&
            E.prerequisiteResourceRole != RequiredRole) {
          llvm::errs()
              << "SPEC_ERROR: conflicting valid-resource "
              << "prerequisites for " << E.id << "\n";
          std::exit(35);
        }
        E.prerequisiteResourceRole = RequiredRole;
      }
      if (!EqC.empty()) EqConstants.insert(EqC);
      if (!NeC.empty()) NeConstants.insert(NeC);
      if (T.ownershipEffect == "ACQUIRE") {
        HasAcquire = true;
        if (!T.toStates.empty()) E.successState = T.toStates.front();
        if (!EqC.empty()) E.successConstant = EqC;
      }
      if (T.ownershipEffect == "RELEASE") {
        HasRelease = true;
        if (!T.toStates.empty()) E.releaseState = T.toStates.front();
      }
      if (!NeC.empty() && (E.successConstant.empty() || NeC == E.successConstant)) {
        if (!T.toStates.empty()) E.failureState = T.toStates.front();
      }
    }
    bool HasPairedReturnSplit = false;
    for (const auto &C : EqConstants) {
      if (!NeConstants.count(C)) continue;
      HasPairedReturnSplit = true;
      if (E.successConstant.empty()) E.successConstant = C;
    }
    if (HasAcquire) E.semanticKind = EventSemanticKind::Init;
    else if (HasRelease) E.semanticKind = EventSemanticKind::End;
    else if (HasPairedReturnSplit) E.semanticKind = EventSemanticKind::Use;
    else if (TransitionCount > 1 &&
             AllOwnershipPreserving &&
             AllStatePreserving &&
             !M.ruleForEvent("D6", E).empty())
      E.semanticKind = EventSemanticKind::OrderedConfiguration;
    else if (TransitionCount == 1) {
      E.semanticKind = EventSemanticKind::StateTransition;
      if (E.successConstant.empty() &&
          EqConstants.size() == 1)
        E.successConstant = *EqConstants.begin();
    } else E.semanticKind = EventSemanticKind::Unsupported;
  }

  auto ContractBuf = llvm::MemoryBuffer::getFile(ContractFile);
  if (!ContractBuf) {
    llvm::errs() << "CONTRACT_ERROR: cannot read " << ContractFile << "\n";
    std::exit(32);
  }
  auto ContractParsed = llvm::json::parse((*ContractBuf)->getBuffer());
  if (!ContractParsed) {
    llvm::errs() << "CONTRACT_ERROR: invalid JSON: "
                 << llvm::toString(ContractParsed.takeError()) << "\n";
    std::exit(33);
  }
  auto *CRoot = ContractParsed->getAsObject();
  if (!CRoot) { llvm::errs() << "CONTRACT_ERROR: root not object\n"; std::exit(34); }
  auto *Codes = CRoot->getArray("unknown_limitation_codes");
  if (!Codes) { llvm::errs() << "CONTRACT_ERROR: limitation codes missing\n"; std::exit(35); }
  for (const auto &V : *Codes) {
    auto *O = V.getAsObject();
    if (!O) continue;
    if (auto C = O->getString("code")) M.limitationCodes.insert(C->str());
  }
  const char *RequiredCodes[] = {
      "U01_UNSUPPORTED_SEMANTICS", "U02_UNRESOLVED_ALIAS",
      "U03_UNRESOLVED_INDIRECT_CALL", "U04_STATE_CAP_EXHAUSTION",
      "U05_MISSING_EVIDENCE", "U06_OUT_OF_MODEL_INTERACTION",
      "U07_UNSUPPORTED_SIDE_EFFECT"};
  for (const char *C : RequiredCodes) {
    if (!M.limitationCodes.count(C)) {
      llvm::errs() << "CONTRACT_ERROR: required limitation code absent: " << C << "\n";
      std::exit(36);
    }
  }
  return M;
}

static SourcePoint sourcePoint(SourceLocation L, const SourceManager &SM) {
  SourcePoint P;
  if (L.isInvalid()) return P;
  SourceLocation E = SM.getExpansionLoc(L);
  PresumedLoc PL = SM.getPresumedLoc(E);
  if (PL.isInvalid()) return P;
  P.file = llvm::sys::path::filename(PL.getFilename()).str();
  P.line = PL.getLine();
  P.column = PL.getColumn();
  if (E.isValid() && E.isFileID()) P.offset = SM.getFileOffset(E);
  return P;
}

static std::string sourceText(const Expr *E, const SourceManager &SM,
                              const LangOptions &LO) {
  if (!E) return "";
  SourceLocation B = SM.getExpansionLoc(E->getBeginLoc());
  SourceLocation End = SM.getExpansionLoc(E->getEndLoc());
  if (B.isInvalid() || End.isInvalid()) return "";
  bool Invalid = false;
  llvm::StringRef R = Lexer::getSourceText(
      CharSourceRange::getTokenRange(B, End), SM, LO, &Invalid);
  if (!Invalid && !R.empty()) return R.str();
  std::string S;
  llvm::raw_string_ostream OS(S);
  PrintingPolicy PP(LO);
  E->printPretty(OS, nullptr, PP);
  OS.flush();
  return S;
}

static std::string immediateMacroName(const Expr *E, const SourceManager &SM,
                                      const LangOptions &LO) {
  if (!E) return "";
  SourceLocation L = E->getExprLoc();
  if (L.isInvalid() || !L.isMacroID()) return "";
  return Lexer::getImmediateMacroName(L, SM, LO).str();
}

static bool isZStreamRecord(QualType T) {
  QualType C = T.getCanonicalType().getUnqualifiedType();
  if (const auto *RT = C->getAs<RecordType>()) {
    const RecordDecl *RD = RT->getDecl();
    return RD && RD->getName() == "z_stream_s";
  }
  return false;
}

static bool isZStreamPointer(QualType T) {
  QualType C = T.getCanonicalType().getUnqualifiedType();
  if (const auto *PT = C->getAs<PointerType>())
    return isZStreamRecord(PT->getPointeeType());
  return false;
}

struct ResourceIdentity {
  bool supported = false;
  std::string id;
  std::string expression;
  std::string limitationCode;
  std::string limitationReason;
};

static ResourceIdentity normalizeResourceExpr(const Expr *Arg,
                                              const SourceManager &SM,
                                              const LangOptions &LO) {
  ResourceIdentity R;
  R.expression = sourceText(Arg, SM, LO);
  const Expr *E = Arg ? Arg->IgnoreParenImpCasts() : nullptr;
  if (!E) {
    R.limitationCode = "U05_MISSING_EVIDENCE";
    R.limitationReason = "resource argument expression unavailable";
    return R;
  }
  if (const auto *U = dyn_cast<UnaryOperator>(E)) {
    if (U->getOpcode() == UO_AddrOf) {
      const Expr *Sub = U->getSubExpr()->IgnoreParenImpCasts();
      if (const auto *D = dyn_cast<DeclRefExpr>(Sub)) {
        if (const auto *VD = dyn_cast<VarDecl>(D->getDecl())) {
          if (!isa<ParmVarDecl>(VD) && VD->hasLocalStorage() && isZStreamRecord(VD->getType())) {
            R.supported = true;
            R.id = "local:" + VD->getNameAsString();
            return R;
          }
        }
      }
    }
  }
  if (const auto *D = dyn_cast<DeclRefExpr>(E)) {
    if (const auto *VD = dyn_cast<VarDecl>(D->getDecl())) {
      if (isZStreamPointer(VD->getType())) {
        R.limitationCode = "U02_UNRESOLVED_ALIAS";
        R.limitationReason = "z_stream pointer/parameter alias is outside the initial direct-local identity slice";
        return R;
      }
    }
  }
  R.limitationCode = "U02_UNRESOLVED_ALIAS";
  R.limitationReason = "resource expression is not a supported direct &local-z_stream identity";
  return R;
}

class ContainsCallVisitor : public RecursiveASTVisitor<ContainsCallVisitor> {
 public:
  explicit ContainsCallVisitor(const CallExpr *Target) : Target(Target) {}
  bool VisitCallExpr(CallExpr *CE) {
    if (CE == Target) Found = true;
    return !Found;
  }
  bool found() const { return Found; }
 private:
  const CallExpr *Target;
  bool Found = false;
};

static bool stmtContainsCall(const Stmt *S, const CallExpr *CE) {
  if (!S) return false;
  ContainsCallVisitor V(CE);
  V.TraverseStmt(const_cast<Stmt *>(S));
  return V.found();
}

struct AssignmentBinding {
  std::string variable;
  bool resultUsedDirectlyInCondition = false;
  std::string conditionText;
};

static AssignmentBinding findAssignmentAndCondition(const CallExpr *CE,
                                                    ASTContext &Ctx,
                                                    const SourceManager &SM,
                                                    const LangOptions &LO) {
  AssignmentBinding B;
  DynTypedNode Node = DynTypedNode::create(*CE);
  for (unsigned Depth = 0; Depth < 12; ++Depth) {
    auto Parents = Ctx.getParents(Node);
    if (Parents.empty()) break;
    const DynTypedNode &P = Parents[0];
    if (const auto *VD = P.get<VarDecl>()) {
      if (VD->hasInit() && stmtContainsCall(VD->getInit(), CE))
        B.variable = VD->getNameAsString();
    }
    if (const auto *BO = P.get<BinaryOperator>()) {
      if (BO->isAssignmentOp() && stmtContainsCall(BO->getRHS(), CE)) {
        const Expr *L = BO->getLHS()->IgnoreParenImpCasts();
        if (const auto *D = dyn_cast<DeclRefExpr>(L)) {
          if (const auto *VD = dyn_cast<VarDecl>(D->getDecl()))
            B.variable = VD->getNameAsString();
        }
      }
    }
    if (const auto *IF = P.get<IfStmt>()) {
      if (stmtContainsCall(IF->getCond(), CE)) {
        B.resultUsedDirectlyInCondition = true;
        B.conditionText = sourceText(IF->getCond(), SM, LO);
      }
    }
    if (const auto *WS = P.get<WhileStmt>()) {
      if (stmtContainsCall(WS->getCond(), CE)) {
        B.resultUsedDirectlyInCondition = true;
        B.conditionText = sourceText(WS->getCond(), SM, LO);
      }
    }
    if (const auto *FS = P.get<ForStmt>()) {
      if (FS->getCond() && stmtContainsCall(FS->getCond(), CE)) {
        B.resultUsedDirectlyInCondition = true;
        B.conditionText = sourceText(FS->getCond(), SM, LO);
      }
    }
    if (const auto *E = P.get<Expr>()) Node = DynTypedNode::create(*E);
    else if (const auto *S = P.get<Stmt>()) Node = DynTypedNode::create(*S);
    else if (const auto *D = P.get<Decl>()) Node = DynTypedNode::create(*D);
    else break;
  }
  return B;
}

struct Limitation {
  std::string code;
  std::string reason;
  std::string function;
  SourcePoint location;
  std::string relatedEvent;
};

struct CallRecord {
  const CallExpr *node = nullptr;
  const EventSpec *event = nullptr;
  std::string qualifiedCallee;
  std::string spelledCallee;
  std::string function;
  SourcePoint location;
  std::vector<std::string> arguments;
  std::string resourceExpression;
  std::string resourceId;
  std::string resourceLimitationCode;
  std::string resourceLimitationReason;
  std::string assignedReturnVariable;
  bool resultUsedDirectlyInCondition = false;
  std::string directConditionText;
  int cfgBlock = -1;
  std::string prerequisiteResourceExpression;
  std::string prerequisiteResourceId;
  std::string prerequisiteResourceLimitationCode;
  std::string prerequisiteResourceLimitationReason;
};

struct NonEventCall {
  const CallExpr *node = nullptr;
  std::string callee;
  SourcePoint location;
};

class CallCollector : public RecursiveASTVisitor<CallCollector> {
 public:
  CallCollector(ASTContext &Ctx, const SpecModel &Spec,
                const FunctionDecl *FD, std::vector<CallRecord> &Calls,
                std::vector<NonEventCall> &OtherCalls,
                std::vector<Limitation> &Limitations)
      : Ctx(Ctx), Spec(Spec), FD(FD), SM(Ctx.getSourceManager()),
        LO(Ctx.getLangOpts()), Calls(Calls), OtherCalls(OtherCalls),
        Limitations(Limitations) {}

  bool VisitCallExpr(CallExpr *CE) {
    SourceLocation L = SM.getExpansionLoc(CE->getExprLoc());
    if (L.isInvalid() || !SM.isWrittenInMainFile(L)) return true;
    const FunctionDecl *Callee = CE->getDirectCallee();
    if (!Callee) {
      Limitation X;
      X.code = "U03_UNRESOLVED_INDIRECT_CALL";
      X.reason = "indirect call target is unresolved in the initial bounded slice";
      X.function = FD->getQualifiedNameAsString();
      X.location = sourcePoint(CE->getExprLoc(), SM);
      Limitations.push_back(std::move(X));
      return true;
    }

    std::vector<std::string> Candidates;
    std::string Macro = immediateMacroName(CE->getCallee(), SM, LO);
    if (!Macro.empty()) Candidates.push_back(Macro);
    std::string CallMacro = immediateMacroName(CE, SM, LO);
    if (!CallMacro.empty()) Candidates.push_back(CallMacro);
    Candidates.push_back(Callee->getNameAsString());
    Candidates.push_back(Callee->getQualifiedNameAsString());
    std::string CalleeText = trimCopy(sourceText(CE->getCallee(), SM, LO));
    if (!CalleeText.empty()) Candidates.push_back(CalleeText);

    const EventSpec *Event = nullptr;
    std::string Spelled;
    for (const auto &C : Candidates) {
      std::string Simple = C;
      size_t Pos = Simple.rfind("::");
      if (Pos != std::string::npos) Simple = Simple.substr(Pos + 2);
      if (const EventSpec *E = Spec.eventBySymbol(Simple)) {
        Event = E;
        Spelled = Simple;
        break;
      }
    }

    if (!Event) {
      OtherCalls.push_back({CE, Callee->getQualifiedNameAsString(),
                            sourcePoint(CE->getExprLoc(), SM)});
      return true;
    }

    CallRecord R;
    R.node = CE;
    R.event = Event;
    R.qualifiedCallee = Callee->getQualifiedNameAsString();
    R.spelledCallee = Spelled;
    R.function = FD->getQualifiedNameAsString();
    R.location = sourcePoint(CE->getExprLoc(), SM);
    for (const Expr *A : CE->arguments()) R.arguments.push_back(sourceText(A, SM, LO));

    std::vector<unsigned> ResourceIndexes;
    for (unsigned I = 0; I < Callee->getNumParams() && I < CE->getNumArgs(); ++I) {
      if (isZStreamPointer(Callee->getParamDecl(I)->getType())) ResourceIndexes.push_back(I);
    }
    std::optional<unsigned> ResourceIndex;
    if (ResourceIndexes.size() == 1) {
      ResourceIndex = ResourceIndexes.front();
    } else if (ResourceIndexes.size() > 1 &&
               Event->condition.find("destination resource") != std::string::npos) {
      for (unsigned I : ResourceIndexes) {
        std::string N = Callee->getParamDecl(I)->getNameAsString();
        std::string Lower = N;
        std::transform(Lower.begin(), Lower.end(), Lower.begin(),
                       [](unsigned char C) { return std::tolower(C); });
        if (Lower.find("dest") != std::string::npos) {
          ResourceIndex = I;
          break;
        }
      }
    }
    if (ResourceIndex && *ResourceIndex < CE->getNumArgs()) {
      ResourceIdentity RI = normalizeResourceExpr(CE->getArg(*ResourceIndex), SM, LO);
      R.resourceExpression = RI.expression;
      R.resourceId = RI.id;
      R.resourceLimitationCode = RI.limitationCode;
      R.resourceLimitationReason = RI.limitationReason;
    } else {
      R.resourceLimitationCode = "U05_MISSING_EVIDENCE";
      R.resourceLimitationReason =
          "unable to identify a unique z_stream resource parameter from the real API declaration";
    }

    if (!Event->prerequisiteResourceRole.empty()) {
      std::string RequiredRole =
          Event->prerequisiteResourceRole;
      std::transform(
          RequiredRole.begin(), RequiredRole.end(),
          RequiredRole.begin(),
          [](unsigned char C) { return std::tolower(C); });

      std::optional<unsigned> PrerequisiteIndex;
      for (unsigned I : ResourceIndexes) {
        std::string ParameterName =
            Callee->getParamDecl(I)->getNameAsString();
        std::transform(
            ParameterName.begin(), ParameterName.end(),
            ParameterName.begin(),
            [](unsigned char C) { return std::tolower(C); });
        if (ParameterName == RequiredRole) {
          PrerequisiteIndex = I;
          break;
        }
      }

      if (PrerequisiteIndex &&
          *PrerequisiteIndex < CE->getNumArgs()) {
        ResourceIdentity PI = normalizeResourceExpr(
            CE->getArg(*PrerequisiteIndex), SM, LO);
        R.prerequisiteResourceExpression = PI.expression;
        R.prerequisiteResourceId = PI.id;
        R.prerequisiteResourceLimitationCode =
            PI.limitationCode;
        R.prerequisiteResourceLimitationReason =
            PI.limitationReason;
      } else {
        R.prerequisiteResourceLimitationCode =
            "U05_MISSING_EVIDENCE";
        R.prerequisiteResourceLimitationReason =
            "unable to identify the specification-required "
            "valid-resource parameter from the real API "
            "declaration";
      }
    }

    AssignmentBinding AB = findAssignmentAndCondition(CE, Ctx, SM, LO);
    R.assignedReturnVariable = AB.variable;
    R.resultUsedDirectlyInCondition = AB.resultUsedDirectlyInCondition;
    R.directConditionText = AB.conditionText;
    Calls.push_back(std::move(R));
    return true;
  }

 private:
  ASTContext &Ctx;
  const SpecModel &Spec;
  const FunctionDecl *FD;
  const SourceManager &SM;
  const LangOptions &LO;
  std::vector<CallRecord> &Calls;
  std::vector<NonEventCall> &OtherCalls;
  std::vector<Limitation> &Limitations;
};

class CallPointerCollector : public RecursiveASTVisitor<CallPointerCollector> {
 public:
  explicit CallPointerCollector(std::set<const CallExpr *> &Out) : Out(Out) {}
  bool VisitCallExpr(CallExpr *CE) { Out.insert(CE); return true; }
 private:
  std::set<const CallExpr *> &Out;
};

class VariableWriteCollector : public RecursiveASTVisitor<VariableWriteCollector> {
 public:
  explicit VariableWriteCollector(std::map<std::string, unsigned> &Counts) : Counts(Counts) {}
  bool VisitVarDecl(VarDecl *VD) {
    if (VD->hasLocalStorage() && VD->hasInit()) ++Counts[VD->getNameAsString()];
    return true;
  }
  bool VisitBinaryOperator(BinaryOperator *BO) {
    if (!BO->isAssignmentOp()) return true;
    const Expr *L = BO->getLHS()->IgnoreParenImpCasts();
    if (const auto *D = dyn_cast<DeclRefExpr>(L)) {
      if (const auto *VD = dyn_cast<VarDecl>(D->getDecl())) ++Counts[VD->getNameAsString()];
    }
    return true;
  }
 private:
  std::map<std::string, unsigned> &Counts;
};

struct CFGEdge {
  int target = -1;
  std::string kind;
};

struct BlockRecord {
  int id = -1;
  bool isEntry = false;
  bool isExit = false;
  std::vector<CFGEdge> successors;
  std::vector<int> predecessors;
};

struct FunctionModel {
  const FunctionDecl *decl = nullptr;
  std::unique_ptr<CFG> cfg;
  std::string name;
  SourcePoint location;
  std::vector<BlockRecord> blocks;
  std::vector<CallRecord> calls;
  std::vector<NonEventCall> otherCalls;
  std::vector<Limitation> limitations;
  std::map<std::string, unsigned> variableWriteCounts;
  std::map<std::string, unsigned> modeledReturnWriteCounts;
  bool containsZlibEvent = false;
};

static bool hasOnlyModeledReturnWrites(
    const FunctionModel &F,
    const std::string &Variable) {
  if (Variable.empty()) return false;
  auto All = F.variableWriteCounts.find(Variable);
  auto Modeled = F.modeledReturnWriteCounts.find(Variable);
  return All != F.variableWriteCounts.end() &&
         Modeled != F.modeledReturnWriteCounts.end() &&
         All->second > 0 &&
         All->second == Modeled->second;
}

static void mapCallsToBlocks(FunctionModel &F) {
  std::map<const CallExpr *, int> Mapping;
  for (const CFGBlock *B : *F.cfg) {
    if (!B) continue;
    for (const CFGElement &El : *B) {
      auto CS = El.getAs<CFGStmt>();
      if (!CS) continue;
      std::set<const CallExpr *> Found;
      CallPointerCollector V(Found);
      V.TraverseStmt(const_cast<Stmt *>(CS->getStmt()));
      for (const CallExpr *CE : Found) if (!Mapping.count(CE)) Mapping[CE] = B->getBlockID();
    }
    if (const Stmt *Term = B->getTerminatorCondition()) {
      std::set<const CallExpr *> Found;
      CallPointerCollector V(Found);
      V.TraverseStmt(const_cast<Stmt *>(Term));
      for (const CallExpr *CE : Found) if (!Mapping.count(CE)) Mapping[CE] = B->getBlockID();
    }
  }
  for (auto &C : F.calls) {
    auto It = Mapping.find(C.node);
    if (It != Mapping.end()) C.cfgBlock = It->second;
  }
}

static FunctionModel buildFunctionModel(FunctionDecl *FD, ASTContext &Ctx,
                                        const SpecModel &Spec) {
  FunctionModel F;
  F.decl = FD;
  F.name = FD->getQualifiedNameAsString();
  F.location = sourcePoint(FD->getLocation(), Ctx.getSourceManager());
  CFG::BuildOptions BO;
  F.cfg = CFG::buildCFG(FD, FD->getBody(), &Ctx, BO);
  if (!F.cfg) return F;

  CallCollector CC(Ctx, Spec, FD, F.calls, F.otherCalls, F.limitations);
  CC.TraverseStmt(FD->getBody());
  F.containsZlibEvent = !F.calls.empty();
  VariableWriteCollector VW(F.variableWriteCounts);
  VW.TraverseStmt(FD->getBody());

  for (const auto &C : F.calls) {
    if (!C.assignedReturnVariable.empty())
      ++F.modeledReturnWriteCounts[
          C.assignedReturnVariable];
  }

  for (const CFGBlock *B : *F.cfg) {
    if (!B) continue;
    BlockRecord BR;
    BR.id = B->getBlockID();
    BR.isEntry = B == &F.cfg->getEntry();
    BR.isExit = B == &F.cfg->getExit();
    unsigned Index = 0;
    for (auto I = B->succ_begin(); I != B->succ_end(); ++I, ++Index) {
      const CFGBlock *S = *I;
      if (!S) continue;
      CFGEdge E;
      E.target = S->getBlockID();
      if (B->getTerminatorCondition() && B->succ_size() == 2)
        E.kind = Index == 0 ? "true" : "false";
      else
        E.kind = "unconditional";
      BR.successors.push_back(std::move(E));
    }
    for (auto I = B->pred_begin(); I != B->pred_end(); ++I) {
      const CFGBlock *P = *I;
      if (P) BR.predecessors.push_back(P->getBlockID());
    }
    std::sort(BR.successors.begin(), BR.successors.end(),
              [](const CFGEdge &A, const CFGEdge &B) {
                if (A.target != B.target) return A.target < B.target;
                return A.kind < B.kind;
              });
    std::sort(BR.predecessors.begin(), BR.predecessors.end());
    F.blocks.push_back(std::move(BR));
  }
  std::sort(F.blocks.begin(), F.blocks.end(),
            [](const BlockRecord &A, const BlockRecord &B) { return A.id < B.id; });
  mapCallsToBlocks(F);
  std::sort(F.calls.begin(), F.calls.end(), [](const CallRecord &A, const CallRecord &B) {
    if (A.location.offset != B.location.offset) return A.location.offset < B.location.offset;
    if (A.event->id != B.event->id) return A.event->id < B.event->id;
    return A.qualifiedCallee < B.qualifiedCallee;
  });
  return F;
}

struct WitnessStep {
  int block = -1;
  std::string eventId;
  SourcePoint location;
  std::string resourceId;
  std::string stateBefore;
  std::string stateAfter;
  std::string note;
};

struct ResourceSnapshot {
  std::string family;
  std::string state;
  bool acquired = false;
  bool released = false;
  bool unknown = false;
  SourcePoint acquisitionLocation;
  std::string acquisitionEvent;
};

enum class ReturnOutcome { Success, Failure };

struct ReturnFact {
  std::string resourceId;
  std::string eventId;
  std::string successConstant;
  ReturnOutcome outcome = ReturnOutcome::Success;
  bool stable = true;
};

struct PathState {
  std::map<std::string, ResourceSnapshot> resources;
  std::map<std::string, ReturnFact> returnFacts;
  std::vector<int> blockPath;
  std::vector<WitnessStep> witness;
  bool analysisUnknown = false;
};

static std::string semanticKey(const PathState &S) {
  std::ostringstream O;
  for (const auto &KV : S.resources) {
    O << "R:" << KV.first << ':' << KV.second.family << ':' << KV.second.state
      << ':' << KV.second.acquired << ':' << KV.second.released << ':' << KV.second.unknown << ';';
  }
  for (const auto &KV : S.returnFacts) {
    O << "V:" << KV.first << ':' << KV.second.resourceId << ':' << KV.second.eventId
      << ':' << KV.second.successConstant << ':' << static_cast<int>(KV.second.outcome)
      << ':' << KV.second.stable << ';';
  }
  O << "U:" << S.analysisUnknown;
  return O.str();
}

struct Observation {
  std::string status; // VALID, VIOLATION, UNKNOWN
  std::string ruleId;
  std::string defectCategory;
  std::string reason;
  std::string function;
  std::string resourceId;
  std::string eventId;
  SourcePoint location;
  std::vector<int> blockPath;
  std::vector<WitnessStep> witness;
  std::string limitationCode;
};

struct Judgment {
  std::string verdict;
  std::vector<std::string> ruleIds;
  std::string defectCategory;
  std::string reason;
  std::string function;
  std::string resourceId;
  std::string eventId;
  SourcePoint location;
  std::vector<int> blockPath;
  std::vector<WitnessStep> witness;
  std::vector<std::string> limitationCodes;
};

struct BranchPredicate {
  bool supported = false;
  std::string variable;
  bool equality = true;
  std::string constantText;
};

static BranchPredicate parseBranchPredicate(const Expr *Condition,
                                            const SourceManager &SM,
                                            const LangOptions &LO) {
  BranchPredicate P;
  if (!Condition) return P;
  const Expr *E = Condition->IgnoreParenImpCasts();
  const auto *BO = dyn_cast<BinaryOperator>(E);
  if (!BO || (BO->getOpcode() != BO_EQ && BO->getOpcode() != BO_NE)) return P;
  const Expr *L = BO->getLHS()->IgnoreParenImpCasts();
  const Expr *R = BO->getRHS()->IgnoreParenImpCasts();
  const DeclRefExpr *D = dyn_cast<DeclRefExpr>(L);
  const Expr *Other = R;
  if (!D) {
    D = dyn_cast<DeclRefExpr>(R);
    Other = L;
  }
  if (!D) return P;
  const auto *VD = dyn_cast<VarDecl>(D->getDecl());
  if (!VD) return P;
  P.variable = VD->getNameAsString();
  P.equality = BO->getOpcode() == BO_EQ;
  P.constantText = immediateMacroName(Other, SM, LO);
  if (P.constantText.empty()) P.constantText = trimCopy(sourceText(Other, SM, LO));
  P.supported = !P.variable.empty() && !P.constantText.empty();
  return P;
}

static bool branchAllows(const BranchPredicate &P, const PathState &S,
                         bool TrueEdge) {
  if (!P.supported) return true;
  auto It = S.returnFacts.find(P.variable);
  if (It == S.returnFacts.end() || !It->second.stable) return true;
  const ReturnFact &F = It->second;
  if (P.constantText != F.successConstant) return true;
  bool ConditionTrue = false;
  if (F.outcome == ReturnOutcome::Success)
    ConditionTrue = P.equality;
  else
    ConditionTrue = !P.equality;
  return ConditionTrue == TrueEdge;
}

static bool isLiveAcquired(const ResourceSnapshot &R) {
  return R.acquired && !R.released && !R.unknown;
}

struct FunctionAnalysis {
  std::vector<Judgment> judgments;
  std::vector<Limitation> limitations;
  bool capExhausted = false;
};

static std::string categoryForRule(const SpecModel &Spec, const std::string &Rule) {
  for (const auto &R : Spec.rules) if (R.id == Rule) return R.defectCategory;
  return "";
}

static Judgment aggregateObservations(const std::vector<Observation> &Obs) {
  Judgment J;
  if (Obs.empty()) return J;
  J.function = Obs.front().function;
  J.resourceId = Obs.front().resourceId;
  J.eventId = Obs.front().eventId;
  J.location = Obs.front().location;
  unsigned Valid = 0, Violation = 0, Unknown = 0;
  std::set<std::string> Rules, Codes;
  const Observation *Chosen = &Obs.front();
  for (const auto &O : Obs) {
    if (O.status == "VALID") ++Valid;
    else if (O.status == "VIOLATION") { ++Violation; Chosen = &O; }
    else { ++Unknown; if (!Violation) Chosen = &O; }
    if (!O.ruleId.empty()) Rules.insert(O.ruleId);
    if (!O.limitationCode.empty()) Codes.insert(O.limitationCode);
    if (J.defectCategory.empty() && !O.defectCategory.empty()) J.defectCategory = O.defectCategory;
  }
  if (Violation > 0 && Valid == 0 && Unknown == 0) J.verdict = "VIOLATION-MUST";
  else if (Violation > 0) J.verdict = "VIOLATION-MAY";
  else if (Unknown > 0) J.verdict = "UNKNOWN";
  else J.verdict = "VALID";
  J.ruleIds.assign(Rules.begin(), Rules.end());
  J.limitationCodes.assign(Codes.begin(), Codes.end());
  J.reason = Chosen->reason;
  J.blockPath = Chosen->blockPath;
  J.witness = Chosen->witness;
  return J;
}

static FunctionAnalysis analyzeFunction(FunctionModel &F, ASTContext &Ctx,
                                        const SpecModel &Spec) {
  FunctionAnalysis A;
  A.limitations = F.limitations;
  if (!F.cfg) {
    Limitation L{"U05_MISSING_EVIDENCE", "Clang CFG construction failed", F.name,
                 F.location, ""};
    A.limitations.push_back(std::move(L));
    return A;
  }

  std::map<int, const CFGBlock *> Blocks;
  for (const CFGBlock *B : *F.cfg) if (B) Blocks[B->getBlockID()] = B;
  std::map<int, std::vector<const CallRecord *>> CallsByBlock;
  for (const auto &C : F.calls) {
    if (C.cfgBlock >= 0) CallsByBlock[C.cfgBlock].push_back(&C);
  }
  for (auto &KV : CallsByBlock) {
    std::sort(KV.second.begin(), KV.second.end(), [](const CallRecord *A, const CallRecord *B) {
      return A->location.offset < B->location.offset;
    });
  }

  std::map<int, std::set<std::string>> Seen;
  struct WorkItem { int block; PathState state; };
  std::deque<WorkItem> Q;
  auto Insert = [&](int Block, PathState S) {
    std::string K = semanticKey(S);
    if (Seen[Block].count(K)) return;
    if (Seen[Block].size() >= StateCap) {
      A.capExhausted = true;
      return;
    }
    Seen[Block].insert(K);
    Q.push_back({Block, std::move(S)});
  };
  Insert(F.cfg->getEntry().getBlockID(), PathState{});

  std::map<std::string, std::map<std::string, Observation>> CallObs;
  std::vector<PathState> ExitStates;
  const SourceManager &SM = Ctx.getSourceManager();
  const LangOptions &LO = Ctx.getLangOpts();

  while (!Q.empty()) {
    WorkItem W = std::move(Q.front());
    Q.pop_front();
    auto BI = Blocks.find(W.block);
    if (BI == Blocks.end()) continue;
    const CFGBlock *B = BI->second;
    PathState Base = std::move(W.state);
    if (Base.blockPath.empty() || Base.blockPath.back() != W.block)
      Base.blockPath.push_back(W.block);
    std::vector<PathState> States{std::move(Base)};

    auto CI = CallsByBlock.find(W.block);
    if (CI != CallsByBlock.end()) {
      for (const CallRecord *C : CI->second) {
        std::vector<PathState> Next;
        for (PathState S : States) {
          // A modeled call-result write supersedes the
          // earlier reaching return fact for this variable.
          if (!C->assignedReturnVariable.empty())
            S.returnFacts.erase(
                C->assignedReturnVariable);

          if (C->resourceId.empty()) {
            Observation O;
            O.status = "UNKNOWN";
            O.reason = C->resourceLimitationReason.empty() ?
                "resource identity unsupported" : C->resourceLimitationReason;
            O.function = F.name;
            O.resourceId = C->resourceExpression;
            O.eventId = C->event->id;
            O.location = C->location;
            O.blockPath = S.blockPath;
            O.witness = S.witness;
            O.limitationCode = C->resourceLimitationCode.empty() ?
                "U02_UNRESOLVED_ALIAS" : C->resourceLimitationCode;
            WitnessStep WS;
            WS.block = W.block;
            WS.eventId = C->event->id;
            WS.location = C->location;
            WS.resourceId = C->resourceExpression;
            WS.stateBefore = "UNKNOWN";
            WS.stateAfter = "UNKNOWN";
            WS.note = O.reason;
            O.witness.push_back(std::move(WS));
            CallObs[std::to_string(C->location.offset)][semanticKey(S)] = std::move(O);
            S.analysisUnknown = true;
            Next.push_back(std::move(S));
            continue;
          }

          ResourceSnapshot Current;
          auto RI = S.resources.find(C->resourceId);
          if (RI == S.resources.end()) {
            Current.family = C->event->family;
            Current.state = Spec.initialState;
          } else {
            Current = RI->second;
          }

          if (C->event->semanticKind == EventSemanticKind::Init) {
            auto InitTransitionsFromCurrent = Spec.transitionsFrom(C->event->id, Current.state);
            bool CurrentStateSupportsInit = false;
            for (const TransitionSpec *T : InitTransitionsFromCurrent)
              if (T->ownershipEffect == "ACQUIRE") CurrentStateSupportsInit = true;
            std::string LiveDestinationOverwriteRule =
                Spec.ruleForEvent("D7", *C->event);
            if (!CurrentStateSupportsInit &&
                !LiveDestinationOverwriteRule.empty() &&
                isLiveAcquired(Current)) {
              Observation O;
              O.status = "VIOLATION";
              O.ruleId = LiveDestinationOverwriteRule;
              O.defectCategory =
                  categoryForRule(Spec, O.ruleId);
              O.reason =
                  "acquisition event would overwrite a destination "
                  "that already owns a live modeled state";
              O.function = F.name;
              O.resourceId = C->resourceId;
              O.eventId = C->event->id;
              O.location = C->location;
              O.blockPath = S.blockPath;
              O.witness = S.witness;
              WitnessStep WS;
              WS.block = W.block;
              WS.eventId = C->event->id;
              WS.location = C->location;
              WS.resourceId = C->resourceId;
              WS.stateBefore = Current.state;
              WS.stateAfter = Current.state;
              WS.note = O.reason;
              O.witness.push_back(std::move(WS));
              CallObs[std::to_string(C->location.offset)]
                  [semanticKey(S)] = std::move(O);
              Next.push_back(std::move(S));
              continue;
            }
            if (!CurrentStateSupportsInit) {
              Observation O;
              O.status = "UNKNOWN";
              O.reason = "frozen specification has no supported acquisition transition from the current resource state";
              O.function = F.name; O.resourceId = C->resourceId; O.eventId = C->event->id;
              O.location = C->location; O.blockPath = S.blockPath; O.witness = S.witness;
              O.limitationCode = "U01_UNSUPPORTED_SEMANTICS";
              WitnessStep WS;
              WS.block = W.block; WS.eventId = C->event->id; WS.location = C->location;
              WS.resourceId = C->resourceId; WS.stateBefore = Current.state;
              WS.stateAfter = Current.state; WS.note = O.reason;
              O.witness.push_back(WS);
              CallObs[std::to_string(C->location.offset)][semanticKey(S)] = std::move(O);
              Current.unknown = true; S.resources[C->resourceId] = Current;
              Next.push_back(std::move(S));
              continue;
            }
            if (Current.acquired && !Current.released) {
              Observation O;
              O.status = "UNKNOWN";
              O.reason = "reinitialization of a currently-live resource is outside the initial supported slice";
              O.function = F.name; O.resourceId = C->resourceId; O.eventId = C->event->id;
              O.location = C->location; O.blockPath = S.blockPath; O.witness = S.witness;
              O.limitationCode = "U01_UNSUPPORTED_SEMANTICS";
              CallObs[std::to_string(C->location.offset)][semanticKey(S)] = std::move(O);
              Current.unknown = true; S.resources[C->resourceId] = Current;
              Next.push_back(std::move(S));
              continue;
            }
            if (C->event->successState.empty() || C->event->failureState.empty() ||
                C->event->successConstant.empty()) {
              Observation O;
              O.status = "UNKNOWN"; O.reason = "frozen init transitions are insufficient for success/failure split";
              O.function = F.name; O.resourceId = C->resourceId; O.eventId = C->event->id;
              O.location = C->location; O.blockPath = S.blockPath; O.witness = S.witness;
              O.limitationCode = "U05_MISSING_EVIDENCE";
              CallObs[std::to_string(C->location.offset)][semanticKey(S)] = std::move(O);
              S.analysisUnknown = true; Next.push_back(std::move(S));
              continue;
            }
            bool PrerequisiteDefinitelyInvalid = false;
            if (!C->event->prerequisiteResourceRole.empty()) {
              if (C->prerequisiteResourceId.empty()) {
                Observation O;
                O.status = "UNKNOWN";
                O.reason =
                    C->prerequisiteResourceLimitationReason.empty()
                        ? "required valid-resource identity is unavailable"
                        : C->prerequisiteResourceLimitationReason;
                O.function = F.name;
                O.resourceId = C->resourceId;
                O.eventId = C->event->id;
                O.location = C->location;
                O.blockPath = S.blockPath;
                O.witness = S.witness;
                O.limitationCode =
                    C->prerequisiteResourceLimitationCode.empty()
                        ? "U05_MISSING_EVIDENCE"
                        : C->prerequisiteResourceLimitationCode;
                CallObs[std::to_string(C->location.offset)]
                    [semanticKey(S)] = std::move(O);
                S.analysisUnknown = true;
                Next.push_back(std::move(S));
                continue;
              }

              auto PI =
                  S.resources.find(
                      C->prerequisiteResourceId);
              if (PI != S.resources.end() &&
                  PI->second.unknown) {
                Observation O;
                O.status = "UNKNOWN";
                O.reason =
                    "required valid resource has an uncertain state";
                O.function = F.name;
                O.resourceId = C->resourceId;
                O.eventId = C->event->id;
                O.location = C->location;
                O.blockPath = S.blockPath;
                O.witness = S.witness;
                O.limitationCode = "U01_UNSUPPORTED_SEMANTICS";
                CallObs[std::to_string(C->location.offset)]
                    [semanticKey(S)] = std::move(O);
                S.analysisUnknown = true;
                Next.push_back(std::move(S));
                continue;
              }

              PrerequisiteDefinitelyInvalid =
                  PI == S.resources.end() ||
                  !isLiveAcquired(PI->second) ||
                  PI->second.family != C->event->family;
            }

            PathState Success = S, Failure = S;
            ResourceSnapshot RS = Current;
            RS.family = C->event->family;
            RS.state = C->event->successState;
            RS.acquired = true; RS.released = false; RS.unknown = false;
            RS.acquisitionLocation = C->location; RS.acquisitionEvent = C->event->id;
            Success.resources[C->resourceId] = RS;
            ResourceSnapshot RF = Current;
            RF.family = C->event->family;
            RF.state = C->event->failureState;
            RF.acquired = false; RF.released = false; RF.unknown = false;
            Failure.resources[C->resourceId] = RF;
            bool Stable =
                hasOnlyModeledReturnWrites(
                    F, C->assignedReturnVariable);
            if (!C->assignedReturnVariable.empty()) {
              Success.returnFacts[C->assignedReturnVariable] =
                  {C->resourceId, C->event->id, C->event->successConstant,
                   ReturnOutcome::Success, Stable};
              Failure.returnFacts[C->assignedReturnVariable] =
                  {C->resourceId, C->event->id, C->event->successConstant,
                   ReturnOutcome::Failure, Stable};
              if (!Stable) {
                Limitation L{"U07_UNSUPPORTED_SIDE_EFFECT",
                    "initialization return variable has multiple writes; branch refinement disabled",
                    F.name, C->location, C->event->id};
                A.limitations.push_back(std::move(L));
              }
            }
            WitnessStep WS;
            WS.block = W.block; WS.eventId = C->event->id; WS.location = C->location;
            WS.resourceId = C->resourceId; WS.stateBefore = Current.state;
            WS.stateAfter = RS.state; WS.note = "spec-derived successful acquisition branch";
            Success.witness.push_back(WS);
            WS.stateAfter = RF.state; WS.note = "spec-derived failed acquisition branch";
            Failure.witness.push_back(WS);
            if (PrerequisiteDefinitelyInvalid) {
              Next.push_back(std::move(Failure));
            } else {
              Next.push_back(std::move(Success));
              Next.push_back(std::move(Failure));
            }
            continue;
          }

          if (C->event->semanticKind == EventSemanticKind::Use) {
            auto TS = Spec.transitionsFrom(C->event->id, Current.state);
            std::string OrderingRule = Spec.ruleForEvent("D6", *C->event);
            Observation O;
            O.function = F.name; O.resourceId = C->resourceId; O.eventId = C->event->id;
            O.location = C->location; O.blockPath = S.blockPath; O.witness = S.witness;
            if (Current.unknown || S.analysisUnknown) {
              O.status = "UNKNOWN"; O.reason = "resource state is uncertain before the stateful zlib use";
              O.limitationCode = "U01_UNSUPPORTED_SEMANTICS";
              Next.push_back(std::move(S));
            } else if (!TS.empty()) {
              O.status = "VALID";
              O.ruleId = Spec.ruleFor("D1", C->event->family, false);
              O.defectCategory = "D1";
              O.reason = "stateful use is preceded by a spec-supported successful live state";
              bool StableReturnFact =
                  hasOnlyModeledReturnWrites(
                      F, C->assignedReturnVariable);
              for (const TransitionSpec *T : TS) {
                if (T->toStates.empty()) continue;
                PathState N = S;
                ResourceSnapshot RN = Current;
                RN.state = T->toStates.front();
                RN.family = C->event->family;
                N.resources[C->resourceId] = RN;
                if (!C->assignedReturnVariable.empty() &&
                    !C->event->successConstant.empty()) {
                  std::string EqC =
                      parseSimpleReturnConstant(T->returnPredicate, "==");
                  std::string NeC =
                      parseSimpleReturnConstant(T->returnPredicate, "!=");
                  if (EqC == C->event->successConstant) {
                    N.returnFacts[C->assignedReturnVariable] =
                        {C->resourceId, C->event->id,
                         C->event->successConstant,
                         ReturnOutcome::Success, StableReturnFact};
                  } else if (NeC == C->event->successConstant) {
                    N.returnFacts[C->assignedReturnVariable] =
                        {C->resourceId, C->event->id,
                         C->event->successConstant,
                         ReturnOutcome::Failure, StableReturnFact};
                  }
                }
                WitnessStep WS;
                WS.block = W.block; WS.eventId = C->event->id; WS.location = C->location;
                WS.resourceId = C->resourceId; WS.stateBefore = Current.state;
                WS.stateAfter = RN.state; WS.note = "spec transition; return not yet refined";
                N.witness.push_back(std::move(WS));
                Next.push_back(std::move(N));
              }
              if (Next.empty()) Next.push_back(std::move(S));
            } else if (Current.state == C->event->failureState ||
                       (!C->event->family.empty() && !Current.acquired && Current.state != Spec.initialState)) {
              O.status = "VIOLATION";
              O.ruleId = Spec.ruleFor("D2", C->event->family, false);
              O.defectCategory = "D2";
              O.reason = "stateful use occurs on a spec-derived failed-initialization state";
              Next.push_back(std::move(S));
            } else if (Current.released) {
              O.status = "VIOLATION";
              O.ruleId = Spec.ruleForCategory("D3");
              O.defectCategory = categoryForRule(Spec, O.ruleId);
              O.reason = "stateful use occurs after the corresponding resource has been released";
              Next.push_back(std::move(S));
            } else if (Current.state == Spec.initialState && !Current.acquired) {
              O.status = "VIOLATION";
              O.ruleId = Spec.ruleFor("D1", C->event->family, false);
              O.defectCategory = "D1";
              O.reason = "stateful use occurs before a successful acquisition";
              Next.push_back(std::move(S));
            } else if (!OrderingRule.empty()) {
              O.status = "VIOLATION";
              O.ruleId = OrderingRule;
              O.defectCategory = categoryForRule(Spec, O.ruleId);
              O.reason = "stateful use has no permitted transition from the current frozen state";
              Next.push_back(std::move(S));
            } else {
              O.status = "UNKNOWN";
              O.reason = "use from this frozen state belongs to an unsupported zlib rule in the current slice";
              O.limitationCode = "U01_UNSUPPORTED_SEMANTICS";
              Next.push_back(std::move(S));
            }
            O.witness = Next.back().witness;
            if (O.witness.empty() || O.witness.back().eventId != C->event->id ||
                O.witness.back().location.offset != C->location.offset) {
              WitnessStep WS;
              WS.block = W.block; WS.eventId = C->event->id; WS.location = C->location;
              WS.resourceId = C->resourceId; WS.stateBefore = Current.state;
              WS.stateAfter = Current.state; WS.note = O.reason;
              O.witness.push_back(std::move(WS));
            }
            CallObs[std::to_string(C->location.offset)][semanticKey(S)] = std::move(O);
            continue;
          }

            if (C->event->semanticKind ==
                EventSemanticKind::OrderedConfiguration) {
              auto TS =
                  Spec.transitionsFrom(
                      C->event->id, Current.state);
              std::string OrderingRule =
                  Spec.ruleForEvent("D6", *C->event);

              Observation O;
              O.function = F.name;
              O.resourceId = C->resourceId;
              O.eventId = C->event->id;
              O.location = C->location;
              O.blockPath = S.blockPath;
              O.witness = S.witness;

              if (!OrderingRule.empty()) {
                O.ruleId = OrderingRule;
                O.defectCategory =
                    categoryForRule(Spec, OrderingRule);
              }

              bool IsAcquisitionReadyState = false;
              for (const auto &Candidate : Spec.events) {
                if (Candidate.semanticKind !=
                    EventSemanticKind::Init)
                  continue;
                if (Candidate.family != Current.family)
                  continue;
                if (Candidate.successState ==
                    Current.state) {
                  IsAcquisitionReadyState = true;
                  break;
                }
              }

              PathState N = S;
              std::string StateAfter = Current.state;
              bool AdvanceState = false;

              if (Current.unknown ||
                  S.analysisUnknown) {
                O.status = "UNKNOWN";
                O.reason =
                    "resource state is uncertain before "
                    "the ordered configuration event";
                O.limitationCode =
                    "U01_UNSUPPORTED_SEMANTICS";
              } else if (OrderingRule.empty()) {
                O.status = "UNKNOWN";
                O.reason =
                    "no event-specific frozen ordering "
                    "rule was resolved";
                O.limitationCode =
                    "U01_UNSUPPORTED_SEMANTICS";
              } else if (TS.empty()) {
                O.status = "VIOLATION";
                O.reason =
                    "ordered configuration event has no "
                    "permitted frozen transition from "
                    "the current resource state";
              } else if (!IsAcquisitionReadyState) {
                O.status = "UNKNOWN";
                O.reason =
                    "the current-state transition requires "
                    "additional frozen preconditions not "
                    "represented by the bounded state, "
                    "including raw-stream boundary evidence";
                O.limitationCode =
                    "U01_UNSUPPORTED_SEMANTICS";
              } else if (
                  TS.size() != 1 ||
                  TS.front()->toStates.size() != 1) {
                O.status = "UNKNOWN";
                O.reason =
                    "ordered configuration transition is "
                    "not uniquely determined by the "
                    "frozen specification";
                O.limitationCode =
                    "U05_MISSING_EVIDENCE";
              } else {
                ResourceSnapshot RN = Current;
                RN.state = TS.front()->toStates.front();
                RN.family = C->event->family;
                N.resources[C->resourceId] = RN;
                StateAfter = RN.state;
                AdvanceState = true;

                O.status = "VALID";
                O.reason =
                    "ordered configuration event is "
                    "applied in the spec-derived "
                    "post-acquisition ready state";
              }

              WitnessStep WS;
              WS.block = W.block;
              WS.eventId = C->event->id;
              WS.location = C->location;
              WS.resourceId = C->resourceId;
              WS.stateBefore = Current.state;
              WS.stateAfter = StateAfter;
              WS.note = O.reason;

              if (AdvanceState) {
                N.witness.push_back(WS);
                O.witness = N.witness;
                Next.push_back(std::move(N));
              } else {
                O.witness.push_back(WS);

                // These frozen transitions have ownership
                // effect NONE. An uncertain ordering
                // judgment must not invent a state change.
                Next.push_back(S);
              }

              CallObs[
                  std::to_string(C->location.offset)]
                  [semanticKey(S)] = std::move(O);
              continue;
            }

          if (C->event->semanticKind == EventSemanticKind::StateTransition) {
            auto TS = Spec.transitionsFrom(C->event->id, Current.state);
            std::string TransitionRule = Spec.ruleForEvent("D5", *C->event);
            Observation O;
            O.function = F.name;
            O.resourceId = C->resourceId;
            O.eventId = C->event->id;
            O.location = C->location;
            O.blockPath = S.blockPath;
            O.witness = S.witness;

            if (Current.unknown || S.analysisUnknown) {
              O.status = "UNKNOWN";
              O.reason = "resource state is uncertain before the state transition";
              O.limitationCode = "U01_UNSUPPORTED_SEMANTICS";
              Next.push_back(std::move(S));
            } else if (TransitionRule.empty()) {
              O.status = "UNKNOWN";
              O.reason = "no frozen obligation maps to this state-transition event";
              O.limitationCode = "U05_MISSING_EVIDENCE";
              Next.push_back(std::move(S));
            } else if (TS.empty()) {
              O.status = "VIOLATION";
              O.ruleId = TransitionRule;
              O.defectCategory = categoryForRule(Spec, O.ruleId);
              O.reason = "state-transition event requires a valid live state with a permitted frozen transition";
              Next.push_back(std::move(S));
            } else {
              const TransitionSpec *Selected = nullptr;
              for (const TransitionSpec *T : TS) {
                if (!T->toStates.empty()) {
                  Selected = T;
                  break;
                }
              }

              if (!Selected) {
                O.status = "UNKNOWN";
                O.ruleId = TransitionRule;
                O.defectCategory = categoryForRule(Spec, O.ruleId);
                O.reason = "frozen state transition has no target state";
                O.limitationCode = "U05_MISSING_EVIDENCE";
                Next.push_back(std::move(S));
              } else {
                PathState Success = S;
                PathState Failure = S;
                ResourceSnapshot RN = Current;
                RN.state = Selected->toStates.front();
                RN.family = C->event->family;
                Success.resources[C->resourceId] = RN;

                bool HasReturnSplit =
                    !C->assignedReturnVariable.empty() &&
                    !C->event->successConstant.empty();
                bool StableReturnFact =
                    HasReturnSplit &&
                    hasOnlyModeledReturnWrites(
                        F, C->assignedReturnVariable);

                if (HasReturnSplit) {
                  Success.returnFacts[
                      C->assignedReturnVariable] =
                      {C->resourceId, C->event->id,
                       C->event->successConstant,
                       ReturnOutcome::Success,
                       StableReturnFact};
                  Failure.returnFacts[
                      C->assignedReturnVariable] =
                      {C->resourceId, C->event->id,
                       C->event->successConstant,
                       ReturnOutcome::Failure,
                       StableReturnFact};

                  if (!StableReturnFact) {
                    Limitation L{
                        "U07_UNSUPPORTED_SIDE_EFFECT",
                        "state-transition return variable "
                        "has unmodeled writes; branch "
                        "refinement disabled",
                        F.name, C->location,
                        C->event->id};
                    A.limitations.push_back(
                        std::move(L));
                  }
                }

                WitnessStep WS;
                WS.block = W.block;
                WS.eventId = C->event->id;
                WS.location = C->location;
                WS.resourceId = C->resourceId;
                WS.stateBefore = Current.state;
                WS.stateAfter = RN.state;
                WS.note =
                    "spec-derived successful "
                    "ownership-preserving state transition";
                Success.witness.push_back(WS);

                O.status = "VALID";
                O.ruleId = TransitionRule;
                O.defectCategory =
                    categoryForRule(Spec, O.ruleId);
                O.reason =
                    "state-transition event has a permitted "
                    "frozen transition from a live state";

                if (HasReturnSplit) {
                  WitnessStep WF = WS;
                  WF.stateAfter = Current.state;
                  WF.note =
                      "spec-derived failed state-transition return; "
                      "prior resource state retained";
                  Failure.witness.push_back(
                      std::move(WF));
                  Next.push_back(
                      std::move(Failure));
                }

                // Keep success last so the call observation
                // retains its successful transition witness.
                Next.push_back(std::move(Success));
              }
            }

            O.witness = Next.back().witness;
            if (O.witness.empty() ||
                O.witness.back().eventId != C->event->id ||
                O.witness.back().location.offset != C->location.offset) {
              WitnessStep WS;
              WS.block = W.block;
              WS.eventId = C->event->id;
              WS.location = C->location;
              WS.resourceId = C->resourceId;
              WS.stateBefore = Current.state;
              WS.stateAfter = Current.state;
              WS.note = O.reason;
              O.witness.push_back(std::move(WS));
            }

            CallObs[std::to_string(C->location.offset)][semanticKey(S)] =
                std::move(O);
            continue;
          }

          if (C->event->semanticKind == EventSemanticKind::End) {
            auto TS = Spec.transitionsFrom(C->event->id, Current.state);
            Observation O;
            O.function = F.name; O.resourceId = C->resourceId; O.eventId = C->event->id;
            O.location = C->location; O.blockPath = S.blockPath; O.witness = S.witness;
            if (Current.unknown || S.analysisUnknown) {
              O.status = "UNKNOWN"; O.reason = "cleanup target state is uncertain";
              O.limitationCode = "U01_UNSUPPORTED_SEMANTICS";
              Next.push_back(std::move(S));
            } else {
              const TransitionSpec *Release = nullptr;
              for (const TransitionSpec *T : TS)
                if (T->ownershipEffect == "RELEASE") { Release = T; break; }
              if (Release && !Release->toStates.empty()) {
                PathState N = S;
                ResourceSnapshot RN = Current;
                RN.state = Release->toStates.front(); RN.released = true; RN.acquired = true;
                N.resources[C->resourceId] = RN;
                WitnessStep WS;
                WS.block = W.block; WS.eventId = C->event->id; WS.location = C->location;
                WS.resourceId = C->resourceId; WS.stateBefore = Current.state;
                WS.stateAfter = RN.state; WS.note = "spec-derived release transition";
                N.witness.push_back(std::move(WS));
                O.status = "VALID";
                O.ruleId = Spec.conditionedCleanupRule();
                O.defectCategory = categoryForRule(Spec, O.ruleId);
                O.reason = "cleanup is applied to a spec-supported successfully acquired live resource";
                Next.push_back(std::move(N));
              } else if (Current.released) {
                O.status = "VIOLATION";
                O.ruleId = Spec.ruleForCategory("D4");
                O.defectCategory = categoryForRule(Spec, O.ruleId);
                O.reason = "cleanup is repeated after the corresponding resource has already been released";
                Next.push_back(std::move(S));
              } else if (!Current.acquired && Current.state != Spec.initialState) {
                O.status = "UNKNOWN";
                O.ruleId = Spec.conditionedCleanupRule();
                O.defectCategory = categoryForRule(Spec, O.ruleId);
                O.reason = "cleanup after failed acquisition is not treated as required or valid by this initial slice";
                O.limitationCode = "U01_UNSUPPORTED_SEMANTICS";
                Next.push_back(std::move(S));
              } else {
                O.status = "UNKNOWN";
                O.reason = "cleanup from this state belongs to an unsupported frozen rule";
                O.limitationCode = "U01_UNSUPPORTED_SEMANTICS";
                Next.push_back(std::move(S));
              }
            }
            O.witness = Next.back().witness;
            if (O.witness.empty() || O.witness.back().eventId != C->event->id ||
                O.witness.back().location.offset != C->location.offset) {
              WitnessStep WS;
              WS.block = W.block; WS.eventId = C->event->id; WS.location = C->location;
              WS.resourceId = C->resourceId; WS.stateBefore = Current.state;
              WS.stateAfter = Current.state; WS.note = O.reason;
              O.witness.push_back(std::move(WS));
            }
            CallObs[std::to_string(C->location.offset)][semanticKey(S)] = std::move(O);
            continue;
          }

          Observation O;
          O.status = "UNKNOWN";
          O.reason = "frozen event exists but its semantics are intentionally unsupported in the initial path-sensitive slice";
          O.function = F.name; O.resourceId = C->resourceId; O.eventId = C->event->id;
          O.location = C->location; O.blockPath = S.blockPath; O.witness = S.witness;
          O.limitationCode = "U01_UNSUPPORTED_SEMANTICS";
          CallObs[std::to_string(C->location.offset)][semanticKey(S)] = std::move(O);
          S.analysisUnknown = true;
          Next.push_back(std::move(S));
        }
        States.swap(Next);
      }
    }

    if (B == &F.cfg->getExit()) {
      for (auto &S : States) ExitStates.push_back(std::move(S));
      continue;
    }

    std::vector<std::pair<int, bool>> Succ;
    unsigned SI = 0;
    for (auto I = B->succ_begin(); I != B->succ_end(); ++I, ++SI) {
      const CFGBlock *SB = *I;
      if (!SB) continue;
      bool TrueEdge = SI == 0;
      Succ.push_back({SB->getBlockID(), TrueEdge});
    }
    const Expr *Cond = dyn_cast_or_null<Expr>(B->getTerminatorCondition());
    BranchPredicate BP = parseBranchPredicate(Cond, SM, LO);
    for (const auto &Dest : Succ) {
      for (const auto &S : States) {
        if (Succ.size() == 2 && BP.supported && !branchAllows(BP, S, Dest.second)) continue;
        Insert(Dest.first, S);
      }
    }
  }

  for (const auto &KV : CallObs) {
    std::vector<Observation> Obs;
    for (const auto &OV : KV.second) Obs.push_back(OV.second);
    Judgment J = aggregateObservations(Obs);
    if (!J.verdict.empty()) A.judgments.push_back(std::move(J));
  }

  std::map<std::string, std::map<std::string, Observation>> CleanupObs;
  for (const auto &S : ExitStates) {
    for (const auto &KV : S.resources) {
      const std::string &Resource = KV.first;
      const ResourceSnapshot &R = KV.second;
      if (!R.acquired) continue; // failed initialization carries no normal cleanup obligation.
      Observation O;
      O.function = F.name; O.resourceId = Resource; O.eventId = "E11_FUNCTION_EXIT";
      O.location = R.acquisitionLocation; O.blockPath = S.blockPath; O.witness = S.witness;
      O.ruleId = Spec.ruleForAcquisition(
          "D5", R.family, R.acquisitionEvent, true);
      O.defectCategory = "D5";
      if (R.unknown || S.analysisUnknown) {
        O.status = "UNKNOWN";
        O.reason = "cleanup obligation cannot be decided because the resource path is uncertain";
        O.limitationCode = "U01_UNSUPPORTED_SEMANTICS";
      } else if (R.released) {
        O.status = "VALID";
        O.reason = "successful acquisition reaches matching release on this relevant exit";
      } else if (isLiveAcquired(R)) {
        O.status = "VIOLATION";
        O.reason = "successful acquisition remains live at a relevant function exit";
      } else {
        O.status = "UNKNOWN";
        O.reason = "successful acquisition reaches an unclassified cleanup state";
        O.limitationCode = "U01_UNSUPPORTED_SEMANTICS";
      }
      CleanupObs[Resource][semanticKey(S)] = std::move(O);
    }
  }
  std::string ConditionalRule = Spec.conditionedCleanupRule();
  for (const auto &KV : CleanupObs) {
    std::vector<Observation> Obs;
    for (const auto &OV : KV.second) Obs.push_back(OV.second);
    Judgment J = aggregateObservations(Obs);
    if (!ConditionalRule.empty()) J.ruleIds.push_back(ConditionalRule);
    std::sort(J.ruleIds.begin(), J.ruleIds.end());
    J.ruleIds.erase(std::unique(J.ruleIds.begin(), J.ruleIds.end()), J.ruleIds.end());
    if (!J.verdict.empty()) A.judgments.push_back(std::move(J));
  }

  if (A.capExhausted) {
    Limitation L{"U04_STATE_CAP_EXHAUSTION",
                 "development abstract-state cap exhausted; no VALID/MUST claim survives for this function",
                 F.name, F.location, ""};
    A.limitations.push_back(std::move(L));
    for (auto &J : A.judgments) {
      J.verdict = "UNKNOWN";
      J.limitationCodes.push_back("U04_STATE_CAP_EXHAUSTION");
      std::sort(J.limitationCodes.begin(), J.limitationCodes.end());
      J.limitationCodes.erase(std::unique(J.limitationCodes.begin(), J.limitationCodes.end()),
                              J.limitationCodes.end());
    }
  }

  std::sort(A.judgments.begin(), A.judgments.end(), [](const Judgment &X, const Judgment &Y) {
    if (X.location.offset != Y.location.offset) return X.location.offset < Y.location.offset;
    if (X.resourceId != Y.resourceId) return X.resourceId < Y.resourceId;
    if (X.eventId != Y.eventId) return X.eventId < Y.eventId;
    return X.verdict < Y.verdict;
  });
  return A;
}

static void addWrapperLimitations(std::vector<FunctionModel> &Functions) {
  std::set<std::string> Wrappers;
  for (const auto &F : Functions) if (F.containsZlibEvent) Wrappers.insert(F.name);
  for (auto &F : Functions) {
    for (const auto &C : F.otherCalls) {
      if (!Wrappers.count(C.callee)) continue;
      Limitation L;
      L.code = "U01_UNSUPPORTED_SEMANTICS";
      L.reason = "call reaches a local wrapper containing zlib events; interprocedural wrapper summaries are not enabled";
      L.function = F.name;
      L.location = C.location;
      F.limitations.push_back(std::move(L));
    }
  }
}

static void emitSourcePoint(const SourcePoint &P) {
  llvm::outs() << "{\"file\":" << jsonString(P.file)
               << ",\"line\":" << P.line << ",\"column\":" << P.column << "}";
}

static void emitWitness(const std::vector<WitnessStep> &W) {
  llvm::outs() << "[";
  for (size_t I = 0; I < W.size(); ++I) {
    if (I) llvm::outs() << ',';
    const auto &S = W[I];
    llvm::outs() << "{\"block_id\":" << S.block
                 << ",\"event_id\":" << jsonString(S.eventId)
                 << ",\"location\":"; emitSourcePoint(S.location);
    llvm::outs() << ",\"resource_id\":" << jsonString(S.resourceId)
                 << ",\"state_before\":" << jsonString(S.stateBefore)
                 << ",\"state_after\":" << jsonString(S.stateAfter)
                 << ",\"note\":" << jsonString(S.note) << "}";
  }
  llvm::outs() << "]";
}

static void emitStringArray(const std::vector<std::string> &V) {
  llvm::outs() << '[';
  for (size_t I = 0; I < V.size(); ++I) {
    if (I) llvm::outs() << ',';
    llvm::outs() << jsonString(V[I]);
  }
  llvm::outs() << ']';
}

static void emitIntArray(const std::vector<int> &V) {
  llvm::outs() << '[';
  for (size_t I = 0; I < V.size(); ++I) {
    if (I) llvm::outs() << ',';
    llvm::outs() << V[I];
  }
  llvm::outs() << ']';
}

class FunctionCollector : public RecursiveASTVisitor<FunctionCollector> {
 public:
  FunctionCollector(ASTContext &Ctx, std::vector<FunctionDecl *> &Out)
      : Ctx(Ctx), SM(Ctx.getSourceManager()), Out(Out) {}
  bool VisitFunctionDecl(FunctionDecl *FD) {
    if (!FD->hasBody()) return true;
    SourceLocation L = SM.getExpansionLoc(FD->getLocation());
    if (L.isInvalid() || !SM.isWrittenInMainFile(L)) return true;
    Out.push_back(FD);
    return true;
  }
 private:
  ASTContext &Ctx;
  SourceManager &SM;
  std::vector<FunctionDecl *> &Out;
};

class SVFConsumer : public ASTConsumer {
 public:
  SVFConsumer(CompilerInstance &CI, const SpecModel &Spec)
      : CI(CI), Spec(Spec) {}

  void HandleTranslationUnit(ASTContext &Ctx) override {
    std::vector<FunctionDecl *> FDs;
    FunctionCollector FC(Ctx, FDs);
    FC.TraverseDecl(Ctx.getTranslationUnitDecl());
    std::sort(FDs.begin(), FDs.end(), [&](const FunctionDecl *A, const FunctionDecl *B) {
      return sourcePoint(A->getLocation(), Ctx.getSourceManager()).offset <
             sourcePoint(B->getLocation(), Ctx.getSourceManager()).offset;
    });

    std::vector<FunctionModel> Functions;
    for (FunctionDecl *FD : FDs) Functions.push_back(buildFunctionModel(FD, Ctx, Spec));
    addWrapperLimitations(Functions);

    std::vector<FunctionAnalysis> Analyses;
    for (auto &F : Functions) Analyses.push_back(analyzeFunction(F, Ctx, Spec));

    llvm::outs() << "{";
    llvm::outs() << "\"schema_version\":\"1.0.0\",";
    llvm::outs() << "\"analyzer_id\":\"semanticverify-clang-cfg-v1\",";
    llvm::outs() << "\"development_snapshot_git_head\":\"UNVERIFIABLE_NO_DOT_GIT\",";
    llvm::outs() << "\"claimed_authoritative_head\":false,";
    llvm::outs() << "\"final_repository_evidence\":false,";
    llvm::outs() << "\"specification\":{";
    llvm::outs() << "\"specification_id\":" << jsonString(Spec.specificationId) << ',';
    llvm::outs() << "\"library_revision\":" << jsonString(Spec.libraryRevision) << ',';
    llvm::outs() << "\"declared_content_sha256\":" << jsonString(Spec.declaredContentSha256) << "},";
    llvm::outs() << "\"state_cap\":" << StateCap << ',';

    llvm::outs() << "\"functions\":[";
    for (size_t FI = 0; FI < Functions.size(); ++FI) {
      if (FI) llvm::outs() << ',';
      const auto &F = Functions[FI];
      llvm::outs() << "{\"name\":" << jsonString(F.name) << ",\"location\":";
      emitSourcePoint(F.location);
      llvm::outs() << ",\"cfg_built\":" << (F.cfg ? "true" : "false") << ",\"blocks\":[";
      for (size_t BI = 0; BI < F.blocks.size(); ++BI) {
        if (BI) llvm::outs() << ',';
        const auto &B = F.blocks[BI];
        llvm::outs() << "{\"block_id\":" << B.id
                     << ",\"entry\":" << (B.isEntry ? "true" : "false")
                     << ",\"exit\":" << (B.isExit ? "true" : "false")
                     << ",\"successors\":[";
        for (size_t EI = 0; EI < B.successors.size(); ++EI) {
          if (EI) llvm::outs() << ',';
          llvm::outs() << "{\"block_id\":" << B.successors[EI].target
                       << ",\"edge\":" << jsonString(B.successors[EI].kind) << "}";
        }
        llvm::outs() << "],\"predecessors\":"; emitIntArray(B.predecessors); llvm::outs() << "}";
      }
      llvm::outs() << "]}";
    }
    llvm::outs() << "],";

    llvm::outs() << "\"calls\":[";
    bool FirstCall = true;
    for (const auto &F : Functions) {
      for (const auto &C : F.calls) {
        if (!FirstCall) llvm::outs() << ',';
        FirstCall = false;
        llvm::outs() << "{\"event_id\":" << jsonString(C.event->id)
                     << ",\"qualified_callee\":" << jsonString(C.qualifiedCallee)
                     << ",\"spelled_callee\":" << jsonString(C.spelledCallee)
                     << ",\"containing_function\":" << jsonString(C.function)
                     << ",\"source_location\":"; emitSourcePoint(C.location);
        llvm::outs() << ",\"arguments\":"; emitStringArray(C.arguments);
        llvm::outs() << ",\"resource_expression\":" << jsonString(C.resourceExpression)
                     << ",\"resource_identity\":" << jsonString(C.resourceId)
                     << ",\"assigned_return_variable\":" << jsonString(C.assignedReturnVariable)
                     << ",\"result_used_directly_in_condition\":"
                     << (C.resultUsedDirectlyInCondition ? "true" : "false")
                     << ",\"direct_condition\":" << jsonString(C.directConditionText)
                     << ",\"cfg_block_id\":" << C.cfgBlock;
        if (!C.resourceLimitationCode.empty()) {
          llvm::outs() << ",\"resource_limitation\":{\"code\":"
                       << jsonString(C.resourceLimitationCode) << ",\"reason\":"
                       << jsonString(C.resourceLimitationReason) << "}";
        }
        llvm::outs() << "}";
      }
    }
    llvm::outs() << "],";

    llvm::outs() << "\"limitations\":[";
    bool FirstLim = true;
    for (size_t FI = 0; FI < Functions.size(); ++FI) {
      std::vector<Limitation> L = Functions[FI].limitations;
      L.insert(L.end(), Analyses[FI].limitations.begin(), Analyses[FI].limitations.end());
      std::sort(L.begin(), L.end(), [](const Limitation &A, const Limitation &B) {
        return std::tie(A.location.offset, A.code, A.reason) <
               std::tie(B.location.offset, B.code, B.reason);
      });
      std::set<std::string> SeenL;
      for (const auto &X : L) {
        std::string K = std::to_string(X.location.offset) + "|" + X.code + "|" + X.reason;
        if (!SeenL.insert(K).second) continue;
        if (!FirstLim) llvm::outs() << ',';
        FirstLim = false;
        llvm::outs() << "{\"code\":" << jsonString(X.code)
                     << ",\"reason\":" << jsonString(X.reason)
                     << ",\"function\":" << jsonString(X.function)
                     << ",\"location\":"; emitSourcePoint(X.location);
        llvm::outs() << ",\"related_event\":" << jsonString(X.relatedEvent) << "}";
      }
    }
    llvm::outs() << "],";

    llvm::outs() << "\"judgments\":[";
    bool FirstJ = true;
    unsigned JID = 1;
    for (const auto &A : Analyses) {
      for (const auto &J : A.judgments) {
        if (!FirstJ) llvm::outs() << ',';
        FirstJ = false;
        char Buf[32];
        std::snprintf(Buf, sizeof(Buf), "J%04u", JID++);
        llvm::outs() << "{\"judgment_id\":" << jsonString(Buf)
                     << ",\"verdict\":" << jsonString(J.verdict)
                     << ",\"rule_ids\":"; emitStringArray(J.ruleIds);
        llvm::outs() << ",\"defect_category\":" << jsonString(J.defectCategory)
                     << ",\"reason\":" << jsonString(J.reason)
                     << ",\"function\":" << jsonString(J.function)
                     << ",\"resource_id\":" << jsonString(J.resourceId)
                     << ",\"event_id\":" << jsonString(J.eventId)
                     << ",\"source_location\":"; emitSourcePoint(J.location);
        llvm::outs() << ",\"cfg_block_path\":"; emitIntArray(J.blockPath);
        llvm::outs() << ",\"limitation_codes\":"; emitStringArray(J.limitationCodes);
        llvm::outs() << ",\"witness\":"; emitWitness(J.witness);
        llvm::outs() << "}";
      }
    }
    llvm::outs() << "]}" << '\n';
  }

 private:
  CompilerInstance &CI;
  const SpecModel &Spec;
};

class SVFAction : public ASTFrontendAction {
 public:
  explicit SVFAction(const SpecModel &Spec) : Spec(Spec) {}
  std::unique_ptr<ASTConsumer> CreateASTConsumer(CompilerInstance &CI,
                                                llvm::StringRef) override {
    return std::make_unique<SVFConsumer>(CI, Spec);
  }
 private:
  const SpecModel &Spec;
};

class SVFActionFactory : public FrontendActionFactory {
 public:
  explicit SVFActionFactory(const SpecModel &Spec) : Spec(Spec) {}
  std::unique_ptr<FrontendAction> create() override {
    return std::make_unique<SVFAction>(Spec);
  }
 private:
  const SpecModel &Spec;
};

} // namespace

int main(int argc, const char **argv) {
  auto ParserExpected = CommonOptionsParser::create(argc, argv, SVFCategory);
  if (!ParserExpected) {
    llvm::errs() << llvm::toString(ParserExpected.takeError()) << '\n';
    return 2;
  }
  SpecModel Spec = loadSpecAndContract(SpecPath, ContractPath);
  CommonOptionsParser &Parser = ParserExpected.get();
  ClangTool Tool(Parser.getCompilations(), Parser.getSourcePathList());
  SVFActionFactory Factory(Spec);
  return Tool.run(&Factory);
}
