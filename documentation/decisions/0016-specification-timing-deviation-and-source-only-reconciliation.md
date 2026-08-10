# Decision 0016: Specification-Timing Deviation and Source-Only Reconciliation

Status: Accepted before library-specific specification authoring

## Confirmed deviation

The frozen protocol-obligation framework requires library-specific protocol
files to be frozen before generated experimental drivers are opened or
annotated, and the preregistered separation policy also treated generated
experimental drivers as prohibited evidence before specification freeze.

After the 800-attempt primary corpus had been generated and compiled and after
the deterministic 140-driver gold sample had been frozen, an audit discovered
that no schema-valid library-specific protocol specification had ever been
committed for zlib, libpcap, curl, cJSON, libtiff, libvpx, c-ares, or lcms.

Current Git history, reflogs, unreachable objects, known historical object
identifiers, and available external project copies contained no recoverable
schema-valid specification for any of the eight libraries.

This is therefore a real specification-timing preregistration deviation.
It must not be represented as restoration of a previously frozen artifact.

## Why recovery remains possible

At discovery of the deviation:

- generated-driver source had not been human-inspected for annotation or
  semantic specification work;
- no gold annotation had started and no gold label existed;
- no SemanticVerify-Fuzz analyzer implementation or output existed;
- no baseline output had been exposed;
- no repair implementation or repair output existed;
- the 140-driver sample was already deterministically frozen and cannot be
  redrawn.

The missing specifications can therefore still be authored without consulting
the generated corpus or semantic outcomes.

## Frozen recovery method

The project adopts a source-only blinded specification reconciliation.

All eight library-specific protocol specifications must be authored and
independently reviewed before any generated-driver source is opened for human
annotation and before analyzer implementation begins.

Specification authoring may use only the source classes already approved by
the frozen Gate-1A provenance contract:

1. pinned official API documentation already available through frozen or
   predeclared evidence;
2. public headers at the pinned library revision;
3. pinned implementation source;
4. pinned upstream tests;
5. predeclared upstream usage examples.

The frozen library revisions, source/build lock, scenario/API bindings,
protocol-obligation contract, and protocol-specification schema may be used.

The following are prohibited during reconciliation:

- generated experimental driver source or raw responses;
- compiler-log semantic contents from generated drivers;
- selected-driver membership as specification evidence;
- gold labels or annotator observations;
- SemanticVerify-Fuzz output;
- baseline or QuartetFuzz output;
- controlled LLM-review output;
- repair output;
- defect-triggering mutations;
- issue searches or external evidence selected because of an observed
  generated-driver failure;
- post-hoc tuning of rules to generated-corpus prevalence, compilation
  characteristics, or expected detector performance.

No new generated-driver sampling or reroll is permitted.

## Author and review requirement

Every specification and every obligation rule must satisfy the frozen
provenance fields. A human specification author and a distinct second reviewer
must be attested before final specification freeze.

The second review must explicitly check:

- evidence completeness;
- transition consistency;
- ownership effects;
- terminal states;
- unsupported conditions.

The reviewer cannot certify a specification by inspecting generated-driver
behavior or analyzer output.

## Eight-library freeze rule

The specifications are frozen in the fixed library order:

zlib, libpcap, curl, cJSON, libtiff, libvpx, c-ares, lcms.

All eight must pass the frozen schema and provenance checks before any
selected generated-driver source is released to annotators.

No held-out library specification may be changed after corresponding driver
content becomes visible. A later discovered specification error is retained in
the primary analysis and any correction is secondary sensitivity analysis
only, as required by the frozen Gate-1A contract.

## Reporting consequence

The study must disclose that the library-specific specifications were authored
after corpus generation because of a preregistration implementation omission.
The paper must not claim a strict pre-generation library-specification freeze.

If this source-only reconciliation completes without generated semantic
evidence exposure, the primary verification analysis may proceed as a
deviation-controlled primary analysis, with the timing deviation reported
explicitly.

It must not be described as perfectly or fully preregistered with respect to
library-specific specification timing.

If a specification author or reviewer uses generated-driver content,
gold labels, analyzer/baseline/repair output, or outcome-prompted external
evidence before specification freeze, the affected library loses
confirmatory held-out status and its corresponding result is exploratory.

## Stage boundary

This decision does not itself author a library specification, open a generated
driver, start annotation, implement the analyzer, run baselines, or implement
repair.

The next allowed operation is a read-only audit of the pinned source snapshots
and an attested specification-author/reviewer start guard. Specification
authoring begins only after that guard is frozen.
