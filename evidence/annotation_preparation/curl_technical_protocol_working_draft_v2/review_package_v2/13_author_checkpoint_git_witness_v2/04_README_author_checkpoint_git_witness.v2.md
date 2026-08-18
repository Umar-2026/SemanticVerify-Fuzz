# curl Technical V2 Author-Checkpoint Minimal Git Witness

This directory provides a self-contained minimal Git-object witness for the
exact V2 author checkpoint.

It contains only the objects required to resolve:

- author commit → author tree;
- author tree → V2 draft blob;
- author tree → Decision 0030 blob.

The parent commit object is deliberately not included.

Run:

`python3 03_verify_author_checkpoint_git_witness.v2.py`
