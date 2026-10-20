# Ultimatic Mode Specification

A hardware-independent specification of Ultimatic CW keying for developers implementing a keyer in their own devices. Ultimatic lets a held paddle remain pressed while the opposite paddle takes control; it does not automatically alternate elements during a squeeze.

**[Read the full specification →](docs/ULTIMATIC_MODE_SPECIFICATION_UNAMBIGUOUS.md)**

**Updated 2026-10-20:** accepts both same-type re-closure policies and restores the two-tap C.2 example alongside held squeeze, with checks for both variants. [See what changed.](CHANGELOG.md)

The document includes the selection and memory rules, reference pseudocode, conformance tests, timing diagrams, and the historical QST source. Start with Sections 3–10 for behavior, Section 12 for scenarios, or Annex C for worked examples. To check the reference sketch or reuse its timelines in your implementation, see the [reference check guide](tests/README.md).

## Scope and status

Revision 2026-10-20 accepts two documented same-type re-closure policies: remembering a new press, or suppressing it during the current element cycle. Section 10.1 explains the historical interpretation and operational rationale; C.2/C.2a compare held squeeze and two taps. Neither policy is presented as an electrically verified reproduction of the 1955 hardware.

Questions, reproducible input timelines and reports of implementation differences are welcome in Issues.

## License and authorship

The specification is licensed under [CC BY 4.0](LICENSE). The historical QST excerpt in Annex A is a separately authored source; the repository license does not relicense that excerpt.

Original document: Paweł (SP5DNA) + Claude AI. Revisions 2026-10-19 and 2026-10-20 prepared with Codex following the author's decisions.
