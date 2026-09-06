# Decision 0253 — authorize C3 bounded candidate content adjudication without execution

D0253 authorizes C3 bounded candidate-content adjudication over exactly the ten frozen D0251 snapshot outputs.

The adjudication universe is metadata-bound by SHA-256:

`dbb16ce946761f76490f86ee7f72a8be3871a72f3ea3c3d25d28ffb67307d7b5`

D0254 is the designated execution decision.

D0253 performs no snapshot-content read, no semantic adjudication, no source-authority determination, no crosswalk-semantic determination, no candidate-admissibility determination, and no Req06/Req14 determination.

Original candidate/source blobs remain closed. Repository search, Git-history search, discovery-root re-enumeration, external network access, reference following, and Python snapshot execution remain prohibited.

C4, C5, C6 and B2 remain unauthorized.

Before any D0254 snapshot-content read, D0253 must first pass a separate independent read-only checkpoint.
