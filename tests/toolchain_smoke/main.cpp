#include <memory>

#include "clang/AST/ASTContext.h"
#include "clang/AST/Decl.h"
#include "clang/Analysis/CFG.h"
#include "clang/Tooling/Tooling.h"
#include "llvm/Support/Casting.h"

int main() {
  std::unique_ptr<clang::ASTUnit> ast =
      clang::tooling::buildASTFromCode(
          "int target(int value) { "
          "if (value > 0) return 1; "
          "return 0; "
          "}");

  if (!ast) {
    return 1;
  }

  clang::ASTContext &context = ast->getASTContext();

  for (clang::Decl *decl :
       context.getTranslationUnitDecl()->decls()) {
    auto *function = llvm::dyn_cast<clang::FunctionDecl>(decl);

    if (function != nullptr &&
        function->getNameAsString() == "target" &&
        function->hasBody()) {
      std::unique_ptr<clang::CFG> cfg =
          clang::CFG::buildCFG(
              function,
              function->getBody(),
              &context,
              clang::CFG::BuildOptions());

      if (!cfg) {
        return 2;
      }

      return cfg->size() >= 3 ? 0 : 3;
    }
  }

  return 4;
}
