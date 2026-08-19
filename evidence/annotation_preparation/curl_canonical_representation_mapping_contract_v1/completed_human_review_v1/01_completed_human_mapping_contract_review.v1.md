\# curl Canonical Representation Mapping Contract V1 — Independent Human Review Packet

\## Purpose

This packet is for independent human technical review of exact immutable:

`curl\_canonical\_representation\_mapping\_contract.v1.json`

The contract does \*\*not\*\* contain a positive V4-to-canonical mapping.

Its author conclusion is deliberately conservative:

`LOSSLESS\_V4\_TO\_FROZEN\_SCHEMA\_MAPPING\_PROVEN=NO`

`CANONICAL\_MATERIALIZATION\_SAFE=NO`

The reviewer must independently determine whether that conclusion is technically

correct.

Approval of this blocker contract does \*\*not\*\* authorize `curl.json`,

does \*\*not\*\* authorize a new canonical schema, and does \*\*not\*\* approve any

positive mapping algorithm.



\## Exact review target

Package file:

`03\_exact\_mapping\_contract.v1.json`

SHA-256:

`31d606f98f2c819291103ba7403214206ccde1d8e5e0e9103f0659c227622257`

Size:

`10879` bytes

Author checkpoint commit:

`afc2bb285f3b9adef8129f106c1c941b14d6f10c`

Author checkpoint tree:

`ace5a3cd3b2797c7a312403656391aa6da4908bb`



\## Exact technical bindings

Approved curl V4 SHA-256:

`e17ae2ea5a70bdd790c946eb4b89ca37368d749cd7463159e69514d88a50cea8`

Frozen canonical schema SHA-256:

`7eb17eeb8f49b37420d0d1d71539cf0d7cb08241ecf133e7b4139fd130718b34`



\## Decision choices

For every CMR-RR item enter exactly one:

`PASS`

`REVISION\_REQUIRED`

`FAIL`

If revision is required, state the precise required successor correction.

\---



\### CMR-RR01 — Exact contract, approved V4, schema, and authorization bindings

Decision: PASS

Notes: Independently checked the immutable packaged evidence. The exact mapping

contract has SHA-256

31d606f98f2c819291103ba7403214206ccde1d8e5e0e9103f0659c227622257

and size 10879 bytes. The author checkpoint is bound to commit

afc2bb285f3b9adef8129f106c1c941b14d6f10c and tree

ace5a3cd3b2797c7a312403656391aa6da4908bb.



The exact approved V4 has SHA-256

e17ae2ea5a70bdd790c946eb4b89ca37368d749cd7463159e69514d88a50cea8

and size 41033 bytes. The frozen canonical schema has SHA-256

7eb17eeb8f49b37420d0d1d71539cf0d7cb08241ecf133e7b4139fd130718b34.



The canonicalization authorization is consistently bound to target

config/protocol\_specifications/curl.json, repository commit

fc3b85c999199e8b45d683fb675a701444478472, and tree

36122c1345051b023662790099b1dfa7d4ea6ee1. The packaged authorization file

also matches SHA-256

5cd2a3a6b090bd900c2efecfe63d187ad5e6d3660a3819109a69431abfd54926.



The actual packaged files, manifest records, and checksum manifest agree.

No binding mismatch was identified.



Confirm the exact mapping-contract SHA/size, author checkpoint commit/tree,

approved V4 SHA/size, frozen schema SHA, and canonicalization-authorization

binding.



\---



\### CMR-RR02 — Corrected zlib/libpcap pre-freeze candidate precedent

Decision: PASS

Notes: Independently compared the packaged pre-freeze source records, finalization

records, and frozen canonical artifacts for both zlib and libpcap.



For zlib, the pre-freeze source record already contains a

candidate\_specification\_fields object with all 15 required pre-freeze

canonical fields. For libpcap, the pre-freeze source record contains the same

complete 15-field canonical-shaped candidate structure. In both cases, the

states, initial\_state, events, transitions, obligations,

permitted\_exit\_states, and provenance structures therefore existed before

canonical finalization.



For each library, I removed the top-level freeze\_date and content\_sha256

fields and the corresponding freeze\_date and content\_sha256 fields from every

canonical obligation. The resulting object is exactly equal to the packaged

pre-freeze candidate. Obligation counts remain unchanged, and every remaining

obligation field and value is identical.



The finalization records also report protocol\_semantic\_change as false and

identify only freeze\_date and content\_sha256 as added fields. No states,

events, or transitions were reconstructed during finalization, and no

obligation semantics were rewritten.



Canonical completion added only freeze\_date and content\_sha256 at the required

top-level and obligation-level locations. No unexpected addition, removal, or

semantic difference was identified.



Using the packaged zlib and libpcap source/finalization/canonical artifacts,

confirm that each reference library already had a canonical-shaped candidate

before freeze.



Confirm finalization did not reconstruct states/events/transitions and did not

semantically rewrite obligations.



Confirm canonical completion added only the field names `freeze\_date` and

`content\_sha256` at the required top-level and obligation-level locations.



\---



\### CMR-RR03 — Absence of a reference-style canonical candidate in exact curl V4

Decision: PASS

Notes:

Independently inspected exact approved curl V4 with SHA-256

e17ae2ea5a70bdd790c946eb4b89ca37368d749cd7463159e69514d88a50cea8.



A recursive inspection found no key named candidate\_specification\_fields and

no object whose fields equal or contain the complete 15-field pre-freeze

canonical core used by the zlib and libpcap precedent.



At the V4 top level, library is the only field shared with that canonical

core. The canonical payload fields states, initial\_state, events, transitions,

obligations, permitted\_exit\_states, and provenance are absent.



V4 contains source-format resource descriptions, rule families, and exit

obligations, but these do not constitute a reference-style canonical-shaped

candidate. No equivalent pre-freeze canonical candidate was identified.

Confirm exact V4 contains no 15-field reference-style pre-freeze canonical

candidate and no `candidate\_specification\_fields` object equivalent to the

zlib/libpcap precedent.



\---



\### CMR-RR04 — Accounting for all ten approved V4 semantic containers

Decision: PASS

Notes: Independently confirmed that the mapping contract accounts for all ten

approved V4 protocol-semantic containers:



api\_surface, resources, return\_condition\_policy, verdict\_semantics,

defect\_taxonomy, global\_runtime\_rules, easy\_handle\_rules, multi\_handle\_rules,

cross\_resource\_rules, and exit\_obligations.



For each container, I calculated SHA-256 over its canonical JSON

representation using sorted object keys, compact separators, and UTF-8

encoding. The resulting hashes agree exactly with the hashes recorded in the

mapping contract:



api\_surface:

c3ec09ab541ce749c01c492875cb090c9971f79a4dd0fb3ba62649f0a2d437a2



resources:

edfb84299c3d298ee0fa315d15ae059931216255ac9fad171001b63922fd5490



return\_condition\_policy:

c71f6a72a92fa5bf9c193e13edfc008791c72488b1943cbd2c1d7cfad4edecbe



verdict\_semantics:

e7465eea48b881cfbfe3e5f42945b906b41fdb4a8bf893d8a11713a38031dce3



defect\_taxonomy:

b69ee78d6966baddd3d48a75a0823b99df9bea55b9e3eaede31a994a7adc6cef



global\_runtime\_rules:

884e1f9a6e4929ecd889c50943e2950c1b8c91fa9062642ccb249b447219c1e7



easy\_handle\_rules:

e9e49ab502f7e0d46f4c19777a5b55122207d1fada7c52d4aca13d758768d6e6



multi\_handle\_rules:

e865bc0f1140d37339fe900eb3c99c3c62cf18e2ae9f8b6359a5983c1f022aa6



cross\_resource\_rules:

820cc3cb457486679fe950b756e89f8f326acf0f6b3fa501522c011bd400b0b3



exit\_obligations:

d2ce5c2cc24effc1b227384779a14475531f964bc8031872bb7d418902c9ac53



All ten containers are present, none is omitted or substituted, and no

container-hash mismatch was identified.



Confirm the contract binds all ten approved V4 protocol-semantic containers:



\- api\_surface

\- resources

\- return\_condition\_policy

\- verdict\_semantics

\- defect\_taxonomy

\- global\_runtime\_rules

\- easy\_handle\_rules

\- multi\_handle\_rules

\- cross\_resource\_rules

\- exit\_obligations



Confirm their contract hashes agree with exact approved V4.



\---



\### CMR-RR05 — Frozen rule and exit-obligation inventory

Decision: PASS

Notes:

Independently counted the rule-family arrays in exact approved V4.



The global\_runtime\_rules array contains 10 records, identified G01 through

G10. The easy\_handle\_rules array contains 21 records, identified E01 through

E21. The multi\_handle\_rules array contains 29 records, identified M01 through

M29. The cross\_resource\_rules array contains 4 records, identified X01 through

X04.



The total rule count is therefore:



10 + 21 + 29 + 4 = 64 rule records.



The exit\_obligations array contains exactly 3 records, covering EASY\_HANDLE,

MULTI\_HANDLE, and EXPLICIT\_GLOBAL\_CLEANUP\_OBLIGATION.



The blocker contract does not contain a replacement or rewritten rule

inventory. It binds the exact V4 rule-family and exit-obligation containers by

their canonical JSON hashes. Those hashes agree with exact approved V4, so no

rule or exit obligation has been added, removed, substituted, or semantically

modified by the blocker contract.



The frozen inventory is therefore 64 rule records and 3 exit obligations, with

no inventory or semantic mismatch identified.



Confirm exact V4 contains:



\- 10 global-runtime rules;

\- 21 easy-handle rules;

\- 29 multi-handle rules;

\- 4 cross-resource rules;

\- 64 total rule records;

\- 3 exit obligations.



Confirm the blocker contract does not add, remove, or semantically modify any

of those rules.



\---



\### CMR-RR06 — Canonical FSM/provenance records are not already present

Decision: PASS

Notes: Independently inspected exact approved V4 for the canonical FSM, obligation,

and provenance structures required by the frozen schema.



The canonical top-level fields states, initial\_state, events, transitions,

obligations, permitted\_exit\_states, and provenance are all absent.



No schema-shaped canonical event records containing event\_id, event\_kind, and

symbol\_or\_condition are present. No canonical transition records containing

transition\_id, from\_states, event\_id, to\_states, return\_predicate, and

ownership\_effect are present.



V4 also contains no pre-freeze canonical obligation records with the required

canonical obligation field set, and no canonical provenance records containing

evidence\_id, source\_type, path\_or\_url, retrieval\_date,

quoted\_or\_paraphrased\_rationale, and content\_sha256.



V4 does contain source-format state lists under individual resource

descriptions and a separate exit\_obligations semantic container. Those

structures are not the frozen schema's canonical top-level states,

transitions, or obligations representation.



The canonical FSM, obligation projection, permitted-exit-state projection,

and provenance records therefore do not already exist in exact V4.



Confirm exact V4 contains no canonical event records, transition records,

pre-freeze canonical obligation records, or canonical provenance records.



Confirm canonical top-level `states`, `initial\_state`, `events`,

`transitions`, `obligations`, `permitted\_exit\_states`, and `provenance`

arrays/fields are absent.



\---



\### CMR-RR07 — Existing authorization does not permit unreviewed reconstruction

Decision: PASS

Notes: Independently inspected the authorized\_transformation\_boundary in the packaged

canonicalization authorization.



Canonical metadata transformation is authorized. The authorization explicitly

sets each of the following to false: protocol-rule semantic change,

protocol-rule addition, protocol-rule removal, API-surface change,

defect-taxonomy change, machine-verdict-contract change, source-evidence

change, new evidence classes, and synthetic protocol events.



Exact V4 does not already contain the canonical states, initial state, events,

transitions, obligations, permitted exit states, or provenance projection.

Constructing those structures would require unresolved representational

decisions. These include choosing a composite or flattened state model for five

resource components, defining event and transition identities, representing

return- and path-sensitive behavior, projecting ownership and membership

effects, mapping all 64 rules and three exit obligations into the canonical

obligation shape, and constructing per-record evidence and provenance.



Without an exact deterministic mapping that has been separately reviewed,

there is no basis for demonstrating that those operations are metadata-only.

Performing them directly could introduce synthetic events, omit or strengthen

rule semantics, change evidence attribution, or otherwise cross an explicitly

prohibited boundary.



I therefore determine that constructing a new

state/event/transition/obligation projection without a reviewed mapping would

exceed the current safe authorization boundary.



Confirm the current authorization permits canonical metadata transformation

but does not authorize:



\- protocol-rule semantic change;

\- protocol-rule addition;

\- protocol-rule removal;

\- API-surface change;

\- defect-taxonomy change;

\- machine-verdict-contract change;

\- source-evidence change;

\- new evidence classes;

\- synthetic protocol events.



Determine whether constructing a new state/event/transition/obligation

projection without a reviewed mapping would exceed that boundary.



\---



\### CMR-RR08 — Current lossless mapping classification

Decision: PASS

Notes: The current evidence supports both:



LOSSLESS\_V4\_TO\_FROZEN\_SCHEMA\_MAPPING\_PROVEN=NO



and:



CANONICAL\_MATERIALIZATION\_SAFE=NO



Exact V4 contains no reference-style canonical candidate and does not already

contain the required canonical states, initial\_state, events, transitions,

obligations, permitted\_exit\_states, or provenance structures.



V4 represents five resource components, cross-resource membership,

return-sensitive and path-sensitive behavior, 64 heterogeneous rule records,

and three source-format exit obligations. The frozen schema instead requires a

single canonical resource\_kind and fully formed state, event, transition,

obligation, permitted-exit-state, and provenance records.



The reviewed evidence does not specify how to construct the composite state

space, select the initial state, assign event and transition identities,

represent branch and function-exit behavior, project ownership and membership

effects, map every rule into the canonical obligation shape, or create exact

source-evidence and provenance records.



The zlib and libpcap precedent does not supply such a mapping. It demonstrates

only how an already complete canonical-shaped candidate was finalized by

adding freeze\_date and content\_sha256.



I found no exact deterministic positive mapping in the packaged reviewed

evidence and therefore cannot identify a mapping that introduces no new

representational decision. Until such a mapping is separately specified,

reviewed, and shown to preserve all V4 semantics, a lossless mapping is not

proven and canonical materialization is not safe.



Determine whether the current evidence supports:



`LOSSLESS\_V4\_TO\_FROZEN\_SCHEMA\_MAPPING\_PROVEN=NO`



and:



`CANONICAL\_MATERIALIZATION\_SAFE=NO`



If not, identify the exact deterministic mapping already supported by the

reviewed evidence and explain why it introduces no new representational

decision.



\---



\### CMR-RR09 — curl.json materialization boundary

Decision: PASS

Notes: Confirmed that curl.json is not present in the supplied handoff and must remain

uncreated at the current boundary.



The blocker contract defines no positive V4-to-canonical mapping. The reviewed

evidence does not prove a lossless mapping to the frozen schema, and no

separately governed canonical-schema successor has been authorized. The

materialization preconditions are therefore not satisfied.



Although the earlier canonicalization authorization identifies

config/protocol\_specifications/curl.json as the intended target and authorizes

creation in principle, it does not permit semantic change, rule addition or

removal, evidence change, or synthetic protocol events. Those constraints

cannot presently be demonstrated without a reviewed deterministic mapping or

an authorized schema successor.



Approval of this blocker contract would confirm only that direct

materialization is not currently justified. It would not define or approve a

positive mapping, authorize a schema modification or successor, or authorize

creation of curl.json.



curl.json must therefore remain uncreated until either an exact positive

mapping is separately authorized and independently reviewed, or a suitable

canonical-schema successor is separately governed and approved.



Confirm `curl.json` must remain uncreated while no reviewed positive mapping

or separately authorized schema successor exists.



Confirm approval of this blocker contract alone would not authorize

materialization.



\---



\### CMR-RR10 — Required successor direction

Decision: PASS

Notes:The current evidence does not demonstrate a deterministic lossless mapping from

approved V4 to the existing frozen schema. It also does not constitute a

formal proof that every possible mapping to that schema is impossible.

Therefore I do not identify or approve a positive mapping as part of this V1

review.



The immediate technical successor, if the existing frozen schema is to be

retained, must be a separately authorized successor mapping contract. It must

define and independently verify at least:



1\. The exact representation of all five V4 resource components, including

&#x20;  whether canonical states are composite, relational, or otherwise encoded.



2\. The canonical initial state and the complete deterministic state inventory.



3\. The exact mapping of the twelve approved API functions, branch conditions,

&#x20;  return conditions, and function exits into canonical event records.



4\. Deterministic transition identities, from-state and to-state sets, return

&#x20;  predicates, ownership effects, membership effects, and error-state

&#x20;  behavior.



5\. Complete accounting from all 64 V4 rule records and all three exit

&#x20;  obligations into canonical obligations, without adding, removing,

&#x20;  strengthening, weakening, or merging distinct semantics.



6\. Preservation of the V4 machine-verdict contract, including VALID,

&#x20;  VIOLATION-MUST, VIOLATION-MAY, and UNKNOWN, as well as path-sensitive,

&#x20;  return-sensitive, ownership-sensitive, and set-valued-state reasoning.



7\. Exact source-evidence and provenance projection without changing evidence

&#x20;  or introducing a new evidence class.



8\. A machine-checkable forward and reverse accounting proof showing that all

&#x20;  ten V4 semantic containers are preserved without opaque field packing,

&#x20;  synthetic protocol events, or unreviewed representational decisions.



If such a contract demonstrates a deterministic lossless mapping, that exact

mapping must be independently reviewed before it may be used for

materialization.



If the mapping work shows that the frozen schema cannot preserve the approved

V4 semantics—for example because it cannot structurally represent the

multi-resource state model, membership relations, verdict semantics, rule

inventory, or provenance without semantic loss or opaque string encoding—then

a separately governed canonical-schema successor is required.



V1 must remain immutable. It must not be modified or reinterpreted to contain a

positive mapping or a schema change.



Determine which technical successor is required.



If a deterministic lossless mapping to the existing frozen schema is

demonstrably possible, identify the precise mapping that must be placed in a

separately authorized successor mapping contract and independently reviewed.



If the frozen schema cannot losslessly represent approved V4, state whether a

separately governed canonical-schema successor is required.



Do not modify or reinterpret V1 in place.



\---



\## Overall technical review decision



Choose exactly one:



`APPROVE\_MAPPING\_BLOCKER\_CONTRACT`



`REVISION\_REQUIRED`



`FAIL`



Overall decision: APPROVE\_MAPPING\_BLOCKER\_CONTRACT

Notes: I completed the independent technical review of CMR-RR01 through CMR-RR10.

All ten review items received PASS.



The exact contract, approved V4, frozen schema, author checkpoint, and

canonicalization-authorization bindings are consistent. The zlib and libpcap

precedent confirms that their canonical-shaped candidates existed before

freeze and that finalization added only freeze\_date and content\_sha256.



Exact curl V4 contains all ten approved semantic containers, 64 rule records,

and three exit obligations, but it does not contain a reference-style

canonical candidate or the required canonical FSM, obligation, permitted-exit,

and provenance records.



The current authorization does not permit semantic change, rule addition or

removal, evidence change, or synthetic protocol events. No exact deterministic

lossless mapping has been specified or reviewed. The contract therefore

correctly classifies lossless mapping as not proven and canonical

materialization as unsafe at the present boundary.



I approve the V1 negative-feasibility and representation-review gate as an

accurate description of the current technical boundary.



This decision does not approve a positive mapping, does not authorize a

canonical-schema modification or successor, and does not authorize creation of

curl.json. V1 must remain immutable. Any positive mapping or schema successor

must be separately authorized and independently reviewed.





`APPROVE\_MAPPING\_BLOCKER\_CONTRACT` means only that the V1 negative-feasibility

contract accurately describes the current mapping boundary.



It does not approve a positive mapping, does not authorize schema modification,

and does not authorize `curl.json`.



\## Reviewer identity



Reviewer role ID: `Spec-Technical-Reviewer-1`

Human reviewer name: Abdul Raheem Shahzad

Human reviewer signature / recorded confirmation: ARS

Human reviewer date: 19 / August / 2026

\## Evidence quarantine

The reviewer must not use:

\- generated-driver source;

\- selected-sample membership;

\- raw model responses;

\- generated-driver compiler-log semantic content;

\- gold labels;

\- analyzer output;

\- baseline output;

\- LLM-review output;

\- repair output.



\## Post-review rule



No assistant-generated or synthetic human approval is permitted.



After this package is committed, exact mapping-contract V1 remains immutable.



If revision is required, create a separately authorized successor rather than

editing V1 in place.



If the reviewer identifies a valid positive mapping, that mapping must be

placed in a separately authorized successor mapping contract and independently

reviewed before any canonical materialization.



If a canonical-schema successor is required, schema supersession requires its

own explicit governance authorization.



`curl.json` must not be created by this review.



