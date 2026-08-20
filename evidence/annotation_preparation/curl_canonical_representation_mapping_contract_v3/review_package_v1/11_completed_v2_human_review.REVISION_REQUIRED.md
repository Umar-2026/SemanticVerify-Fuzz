# curl Canonical Representation Mapping Contract V2 — Independent Human Review Packet
## Purpose
This packet is for independent human technical review of exact immutable:
`curl_canonical_representation_mapping_contract.v2.json`
The V2 author conclusion is:
`FROZEN_SCHEMA_INSUFFICICIENCY_DEMONSTRATED_SCHEMA_SUCCESSOR_REQUIRED`
This is currently an **author conclusion only**.
The reviewer must independently determine whether the proof establishes that,
under the exact frozen schema and exact authorized losslessness/admissibility
constraints, the approved curl V4 semantics cannot be represented by an
admissible lossless mapping without schema supersession.
The claim is deliberately scoped. It is **not** a claim that every
theoretically imaginable arbitrary string encoding is mathematically
impossible.
Approval of this V2 proof does **not** authorize a schema successor and does
**not** authorize `curl.json`.
## Exact review target
Package file:
`03_exact_v2_mapping_contract.v2.json`
SHA-256:
`f2badbc07895e8baff078a0ce617ceb6ff02d39c7634a9e38b3b8a46a18d811c`
Size:
`18515` bytes
Author checkpoint commit:
`9bc2d448cf2c08a728174090c3d819bbdb9e28f1`
Author checkpoint tree:
`9cb9b34bbeb45cc5916543a04e0f0dad8f54af50`
## Decision choices
For every V2-RR item enter exactly one:
`PASS`
`REVISION_REQUIRED`
`FAIL`
If revision is required, state the exact technical correction required in a
separately governed successor. Do not edit V2 in place.
---
### V2-RR01 — Exact artifact and governance bindings
Decision: REVISION_REQUIRED
Notes: The exact V2 SHA-256 and size, approved V4 SHA, frozen canonical
schema SHA, V2 authorization SHA, V1 mapping-contract SHA,
completed V1 human-review SHA, and completed V1 review-record SHA
were independently recomputed from the immutable review package and
matched the declared bindings.

The author checkpoint commit
9bc2d448cf2c08a728174090c3d819bbdb9e28f1 and tree
9cb9b34bbeb45cc5916543a04e0f0dad8f54af50 are recorded
consistently across the package binding records. However, the supplied
ZIP contains neither the Git repository nor a Git bundle containing
those objects. Their existence, tree relationship, and binding of the
exact V2 bytes at the repository path therefore could not be
independently verified.

Required correction: provide read-only access to the source repository
or a Git bundle containing the author checkpoint commit and its
reachable objects. Do not modify immutable V2.

Confirm the exact V2 SHA/size, author checkpoint commit/tree, approved V4 SHA,
frozen canonical schema SHA, V2 authorization SHA, V1 mapping-contract SHA,
completed V1 human-review SHA, and completed V1 review-record SHA.
Confirm no binding mismatch exists.
---
### V2-RR02 — Scope and logical strength of the insufficiency claim
Decision: PASS
Notes: The exact V2 proof limits its insufficiency conclusion to the exact
frozen canonical schema bound by SHA-256
7eb17eeb8f49b37420d0d1d71539cf0d7cb08241ecf133e7b4139fd130718b34,
the exact approved curl V4 semantics bound by SHA-256
e17ae2ea5a70bdd790c946eb4b89ca37368d749cd7463159e69514d88a50cea8,
and the exact V2 authorization bound by SHA-256
5d3771c4748731642f3068722e986e65479a9b85d1087737e2faeb2dc76b073b.

The required losslessness contract explicitly requires both forward and
reverse semantic accounting, preservation of all 10 approved V4 semantic
containers, all 64 rule records, all 3 exit obligations, the four-verdict
contract, membership sensitivity, path sensitivity, set-valued reasoning,
and first-class UNKNOWN.

The claim_scope expressly states that V2 does not claim every
theoretically imaginable arbitrary-string encoding is mathematically
impossible. Its conclusion applies only to admissible mappings under the
exact frozen schema, exact approved V4 semantics, and exact V2
authorization constraints. No scope or logical-strength overclaim was
identified.

Determine whether V2 correctly limits its conclusion to:
- the exact frozen canonical schema;
- the exact approved curl V4 semantics;
- the exact V2 authorization constraints;
- the requirement for forward and reverse lossless semantic accounting.
Confirm V2 does not overclaim that every imaginable arbitrary encoding is
mathematically impossible.
---
### V2-RR03 — EASY_MULTI_MEMBERSHIP structural obstruction
Decision: PASS
Notes: The exact approved curl V4 contains the identity-sensitive relation
easy_handle -> zero_or_one_multi_handle at
$.resources.EASY_MULTI_MEMBERSHIP. It specifies successful add as
DETACHED -> ATTACHED_TO_SPECIFIC_MULTI, successful remove as
ATTACHED_TO_SPECIFIC_MULTI -> DETACHED, and confirms that add does not
transfer ownership.

The frozen canonical schema is closed with additionalProperties=false.
Its protocol states are strings, and its event and transition structures
contain no first-class source-resource, target-resource, membership,
relation-cardinality, or attached-multi-identity field. Consequently, it
has no typed structural carrier for binding an easy-handle instance to
zero or one specific multi-handle instance.

The authorization permits composite/product-state construction and
membership-effect projection. Those mechanisms can represent coarse
DETACHED/ATTACHED membership status, but the frozen schema still provides
no structural field for the identity of the specific target multi handle
or for reversible parameterized relation semantics.

Packing the missing relation into arbitrary free-form strings is
inadmissible because opaque payload packing is unauthorized. Inventing
semantic events solely to carry membership metadata is inadmissible
because semantic protocol-event invention is unauthorized. Adding a new
first-class membership field would modify or supersede the frozen schema,
which is also unauthorized. The V2-O1 fallback classifications are
therefore consistent with the exact V2 authorization boundary.

Independently assess the V2-O1 witness.
Confirm approved V4 contains the identity-sensitive relation:
`easy_handle -> zero_or_one_multi_handle`
Determine whether the frozen schema contains a first-class structural carrier
for this relation.
Determine whether the proposed inadmissible fallbacks are correctly
classified under the V2 authorization boundary.
---
### V2-RR04 — Four-verdict and feasible-state join obstruction
Decision: PASS
Notes: The exact approved curl V4 verdict_semantics object contains exactly four
allowed machine verdicts: VALID, VIOLATION-MUST, VIOLATION-MAY, and
UNKNOWN. No additional machine verdict is present.

The feasible-state join policy distinguishes mixed state uncertainty from
normative or model-coverage uncertainty. A mixture of VALID and an
enforceable violation joins to VIOLATION-MAY, while unresolved normative
strength or model coverage produces UNKNOWN. The policy also explicitly
requires that UNKNOWN must never silently become VALID.

The V2-O2 witness reproduces the exact four-verdict list and join policy.
Its semantic hash,
e7465eea48b881cfbfe3e5f42945b906b41fdb4a8bf893d8a11713a38031dce3,
matches the V2 binding for the approved V4 verdict_semantics container.

The frozen canonical schema is closed with additionalProperties=false and
contains no explicit machine-verdict, verdict-semantics, feasible-state
join-policy, or UNKNOWN-handling property. Its states, events,
transitions, obligations, ownership-effect values, defect categories, and
severity values serve different protocol purposes. Using those fields for
the machine-verdict and join-policy contract would repurpose their
semantics; serializing the contract into free-form strings would not be a
first-class structural representation and would violate the prohibition
on opaque payload packing.

The frozen schema therefore has no explicit same-purpose first-class
structural carrier for the approved V4 four-verdict and feasible-state
join-policy contract.

Independently assess V2-O2.
Confirm approved V4 contains exactly:
`VALID`
`VIOLATION-MUST`
`VIOLATION-MAY`
`UNKNOWN`
and a feasible-state join policy distinguishing mixed valid/violation states
from normative/model-coverage uncertainty.
Determine whether the frozen schema has an explicit first-class structural
carrier for this machine-verdict and join-policy contract.
---
### V2-RR05 — Path-sensitive and set-valued reasoning obstruction
Decision: PASS
Notes: The exact approved curl V4 representation_policy explicitly requires
path-sensitive analysis, explicit evaluation of known finite feasible-state
alternatives, first-class UNKNOWN, and the rule that UNKNOWN must never be
silently converted to VALID. The corresponding feasible-state join policy
uses a common verdict when all feasible states agree, produces
VIOLATION-MAY for mixed VALID/enforceable-violation states, and reserves
UNKNOWN for unresolved normative strength or model coverage.

These requirements define analysis-machine behavior: maintaining and
evaluating feasible path/state alternatives, joining their verdicts, and
preserving uncertainty soundly. They are not ordinary curl API calls,
protocol state changes, branches, or function-exit events.

The frozen canonical schema supports API_CALL, BRANCH, and FUNCTION_EXIT
events and arrays of protocol transition states, but it contains no
same-purpose structural property for path-sensitive evaluation policy,
finite set-valued analysis, feasible-state join semantics, first-class
machine-verdict UNKNOWN, or the prohibition on converting UNKNOWN to VALID.
A BRANCH event can represent an individual path condition but does not
specify the required analysis or join algorithm. Similarly, from_states
and to_states arrays describe protocol transitions rather than an
analyzer's feasible-state set.

Authorized path-condition and product-state projections therefore do not
supply the missing analysis-policy carrier. Encoding that policy in
protocol state/event strings would repurpose protocol fields or require
prohibited opaque packing. The V2-O3 obstruction is supported.
Independently assess V2-O3.

Confirm approved V4 requires path-sensitive reasoning, explicit finite
set-valued state reasoning, first-class UNKNOWN, and the rule that UNKNOWN
must never silently become VALID.

Determine whether these are analysis-machine semantics rather than ordinary
API protocol events/transitions and whether the frozen schema provides a
same-purpose structural carrier.
---
### V2-RR06 — Structured rule-payload obstruction
Decision: PASS
Notes: Independent enumeration of the four approved V4 rule families found
exactly 12 structured list/dictionary-valued rule-field occurrences:
G01.effect, G02.effect, G03.effect, G05.effect, G06.effect, G07.effect,
E01.effect, E02.effect, E03.effect, E04.runtime_post_state, E12.excludes,
and M15.excludes. This exactly matches the V2-O4 occurrence list and
count.

The canonical obligation item is itself an object, but none of its
individual properties accepts an object-typed value. The independently
derived object-typed obligation-property count is therefore zero. The
existing permitted_transitions and source_evidence fields are arrays of
strings with separately defined purposes and are not generic structured
payload carriers.

Preserving the V4 dictionaries and lists could require a deterministic
structural decomposition into same-purpose canonical states, transitions,
or obligation records. Such a mapping would need explicit forward
accounting and an independently checkable reverse-reconstruction proof,
with no rule loss, addition, strengthening, weakening, or semantic change.
No such positive decomposition is defined in V2.

Absent that separately defined and reversible structural decomposition,
serializing the structured values into free-form canonical strings would
constitute unauthorized opaque payload packing. V2-O4 is therefore
correctly supported as a supporting structural obstruction.

Independently assess V2-O4.
Confirm exact V4 contains 12 structured list/dictionary rule-field
occurrences and that the frozen canonical obligation representation contains
zero object-typed fields.

Determine whether preserving those structured semantics would require either
a separately defined structural decomposition with reverse proof or an
unauthorized opaque encoding.
---
### V2-RR07 — Admissibility of alternative carrier classes
Decision: PASS
Notes: V2 considers the five required alternative carrier classes and classifies
them consistently with the exact authorization boundary.

A new first-class schema field is inadmissible because the frozen schema
is closed with additionalProperties=false and neither schema mutation nor
schema-successor creation is authorized. Opaque free-form string encoding
is inadmissible because opaque payload packing is explicitly unauthorized.

Representational event identifiers for existing approved V4 API, branch,
and function-exit semantics are authorized. V2 correctly distinguishes
those identifiers from inventing new semantic protocol events solely to
carry membership metadata or machine-analysis policy; the latter is
explicitly unauthorized.

Repurposing protocol states, events, transitions, obligations, or exit
states to encode machine-verdict, feasible-state join, or analysis-policy
semantics would change the defined semantic role of those fields and would
not satisfy same-purpose forward and reverse accounting. Such repurposing
is inconsistent with the prohibition on protocol semantic change.

Independent inspection of the frozen schema found no direct same-purpose
first-class structural carrier for the identity-sensitive membership
relation, the four-verdict and feasible-state join contract, or the
path-sensitive/set-valued/UNKNOWN analysis policy. Authorized product-state,
membership, path-condition, and representational-ID projections do not
supply those missing machine-policy and relation carriers without falling
into semantic repurposing or opaque encoding.

The five carrier classes are therefore correctly classified under the
exact V2 authorization constraints.
Review the candidate carrier classes considered by the V2 proof:
- new first-class schema fields;
- opaque free-form string encoding;
- synthetic API/branch/function-exit events;
- repurposing existing protocol fields for machine-policy semantics;
- direct same-purpose structural carriers.

Determine whether V2 correctly classifies each alternative under the exact
authorization constraints.
---
### V2-RR08 — Complete semantic accounting boundary
Decision: REVISION_REQUIRED
Notes: The exact V2 proof correctly binds the 10 approved V4 semantic containers,
12 API functions, 5 resource components, 64 rule records, 3 exit
obligations, and the four machine verdicts. Its required losslessness
contract explicitly requires forward and reverse accounting, membership
sensitivity, path sensitivity, set-valued reasoning, and first-class
UNKNOWN.

However, the exact V2 authorization separately requires both
ownership-sensitive semantics and return-sensitive semantics to be
preserved. Approved V4 confirms these requirements through
representation_policy.ownership_sensitive=true and
representation_policy.return_sensitive=true.

The V2 formal_insufficiency_argument.required_losslessness_contract
contains no ownership_sensitive_semantics_preserved requirement and no
return_sensitive_semantics_preserved requirement. Binding the resources
and return_condition_policy containers by hash preserves their source
contents, but does not explicitly place the separately mandated ownership-
and return-sensitive analysis requirements inside the formal hypothetical
mapping boundary. The representation_policy object is not one of the 10
approved semantic containers, and the V2-O3 required_semantics subset does
not include ownership or return sensitivity.

V2 therefore silently drops two required semantic-accounting requirements
from its formal losslessness contract.

Required correction: keep exact V2 immutable and create a separately
authorized successor that explicitly adds ownership-sensitive and
return-sensitive semantic preservation to the required losslessness
contract. The successor should separately bind the complete exact V4
representation_policy, or otherwise machine-checkably account for all of
its mandatory fields, while retaining the existing 10-container, inventory,
verdict, UNKNOWN, forward-accounting, and reverse-accounting requirements.
No protocol-semantic change is required or authorized.

Confirm the proof binds and preserves the required accounting boundary:
- all 10 approved V4 semantic containers;
- 12 API functions;
- 5 resource components;
- 64 rule records;
- 3 exit obligations;
- four machine verdicts;
- membership sensitivity;
- ownership sensitivity;
- return sensitivity;
- path sensitivity;
- first-class UNKNOWN;
- forward and reverse accounting requirements.
Determine whether the proof silently drops any required V4 semantic class.
---
### V2-RR09 — Technical conclusion under the current frozen schema
Decision: PASS
Notes: The scoped technical conclusion is supported by an independently decisive
obstruction. Exact approved V4 requires the four machine verdicts VALID,
VIOLATION-MUST, VIOLATION-MAY, and UNKNOWN, together with a feasible-state
join policy that distinguishes mixed VALID/enforceable-violation states
from unresolved normative-strength or model-coverage uncertainty and
prohibits silently converting UNKNOWN to VALID.

The frozen canonical schema contains no same-purpose first-class structural
carrier for machine verdicts, feasible-state verdict joining, first-class
UNKNOWN, or the required UNKNOWN-preservation rule.

Adding such fields would modify or supersede the frozen schema. Packing
the contract into free-form strings would use unauthorized opaque payload
encoding. Representing the policy through invented API, branch, or
function-exit events would introduce unauthorized synthetic semantic
events. Encoding machine verdicts or join behavior as protocol states,
transitions, or obligations would repurpose fields with different defined
semantic roles.

The authorized product-state, path-condition, membership-effect, and
representational-ID mechanisms can project existing protocol semantics but
do not provide a same-purpose machine-verdict and join-policy carrier.
No admissible deterministic lossless forward-and-reverse mapping for this
mandatory semantic class was identified.

The RR08 omission of explicit ownership- and return-sensitive preservation
still requires a separately governed successor correction. That omission
does not supply the missing verdict/join carrier and therefore does not
negate the independently supported frozen-schema insufficiency conclusion.
The exact V2 technical conclusion is accepted only within its stated
frozen-schema and authorization scope; it is not a claim about every
theoretically imaginable arbitrary encoding.
Determine whether the evidence supports the scoped conclusion:

`FROZEN_SCHEMA_INSUFFICIENCY_DEMONSTRATED_SCHEMA_SUCCESSOR_REQUIRED`

The conclusion should be accepted only if no admissible same-purpose
structural mapping exists under the exact current constraints without
prohibited opaque packing, synthetic semantic events, semantic-field
repurposing, or schema modification.

If you believe an admissible deterministic lossless mapping already exists,
identify it precisely enough that it could be placed into a separately
authorized successor mapping contract and independently checked forward and
backward.
---
### V2-RR10 — Governance consequence and next boundary
Decision: PASS
Notes:
Exact V2 clearly distinguishes the technical conclusion that a canonical
schema successor is required from governance authorization to create,
author, or adopt such a successor. It records
canonical_schema_successor_required=true while separately recording
canonical_schema_successor_authorized=false and
schema_successor_authorized_by_this_contract=false.

V2 does not authorize schema modification or schema-successor creation.
The exact frozen canonical schema remains independently bound by SHA-256
7eb17eeb8f49b37420d0d1d71539cf0d7cb08241ecf133e7b4139fd130718b34
and is not modified by V2.

V2 defines and approves no positive mapping. It records
positive_mapping_algorithm_defined=false,
positive_mapping_algorithm_approved=false,
positive_mapping_candidate_authored=false, and
lossless_v4_to_frozen_schema_mapping_proven=false.

V2 does not authorize or create curl.json. It records
curl_json_creation_authorized=false, curl_json_created=false, and
canonical_materialization_safe=false. Analyzer implementation, analyzer
execution, baseline execution, and repair also remain unauthorized.

The independent-review requirement states that approval of this proof may
not itself authorize a schema successor. Approval could therefore
establish only the technical need for a separately governed
schema-successor process. A new explicit governance authorization would be
required before any schema-successor authoring could begin.

Exact V2 must remain immutable after review. Its immutability policy states
that, once committed at the author checkpoint, any correction requires a
separately authorized successor rather than an in-place edit. Accordingly,
the correction required by V2-RR08 must be made only in a separately
governed successor artifact; exact V2 must not be changed.

Confirm that approval of this V2 proof would establish only the technical
need for a separately governed schema-successor process.

Confirm V2 itself does not:
- authorize a schema successor;
- modify the frozen schema;
- approve a positive mapping;
- authorize `curl.json`;
- authorize analyzer implementation;
- authorize baseline execution;
- authorize repair.
Confirm exact V2 must remain immutable after review.
---
## Overall technical review decision
Choose exactly one:
`APPROVE_V2_SCHEMA_INSUFFICIENCY_PROOF`
`REVISION_REQUIRED`
`FAIL`

Overall decision: REVISION_REQUIRED
Notes: The scoped technical conclusion that the current frozen canonical schema
is insufficient is supported by the independently decisive absence of a
same-purpose structural carrier for the mandatory four-verdict,
feasible-state join, and first-class UNKNOWN analysis-policy contract.
V2-RR02 through V2-RR07 and V2-RR09 through V2-RR10 pass.

However, exact V2 cannot be approved for two reasons.

First, under V2-RR01, all packaged SHA-256 and size bindings were
independently verified, and the author checkpoint commit and tree values
are internally consistent across the sealed records. The supplied ZIP
contains neither the source Git repository nor a Git bundle, however.
Consequently, commit
9bc2d448cf2c08a728174090c3d819bbdb9e28f1, tree
9cb9b34bbeb45cc5916543a04e0f0dad8f54af50, and the binding of the
exact V2 bytes at the repository path could not be independently
recomputed from Git objects. A read-only repository or Git bundle
containing the checkpoint and reachable objects is required to complete
that verification.

Second, under V2-RR08, the exact V2 authorization explicitly requires
ownership-sensitive and return-sensitive semantics to be preserved.
Approved V4 records ownership_sensitive=true and return_sensitive=true.
The V2 formal required_losslessness_contract explicitly preserves
membership sensitivity, path sensitivity, set-valued reasoning,
first-class UNKNOWN, the four verdicts, and forward/reverse accounting,
but it does not include explicit ownership-sensitive or return-sensitive
preservation requirements. Exact V2 therefore omits two mandatory
semantic-accounting requirements from its formal losslessness boundary.

The Git verification evidence may be supplied through a new immutable
review-package artifact without modifying V2. The semantic-accounting
defect must be corrected only in a separately authorized immutable
successor that explicitly requires ownership-sensitive and
return-sensitive preservation and machine-checkably binds the complete
approved V4 representation-policy boundary.

Exact V2 must remain immutable. This review does not authorize a schema
successor, schema modification, a positive mapping, curl.json, analyzer
implementation or execution, baseline execution, or repair. Any corrected
successor requires separate governance authorization and a new independent
human review.


## Reviewer identity
Reviewer role ID: `Spec-Technical-Reviewer-1`
Human reviewer name: Abdul Raheem Shahzad
Human reviewer signature / recorded confirmation: ARS
Human reviewer date: 20 / August / 2026

## Evidence quarantine
The reviewer must not use:
- generated-driver source;
- selected-sample membership;
- raw model responses;
- generated-driver compiler-log semantic content;
- gold labels;
- analyzer output;
- baseline output;
- LLM-review output;
- repair output.

## Post-review rule
No assistant-generated or synthetic human approval is permitted.
Exact V2 must remain immutable.
If revision is required, create a separately authorized successor rather than
editing V2 in place.
If the reviewer approves the schema-insufficiency proof, schema-successor
authoring still requires a separate explicit governance authorization.
`curl.json` must not be created by this review.