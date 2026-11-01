# Ultimatic Mode Specification

A hardware-independent specification of Ultimatic CW keying for developers implementing a keyer in their own devices. Ultimatic lets a held paddle remain pressed while the opposite paddle takes control; it does not automatically alternate elements during a squeeze.

**[Read the full specification →](docs/ULTIMATIC_MODE_SPECIFICATION_UNAMBIGUOUS.md)**

**Revision:** 2026-11-01 · [Revision history](CHANGELOG.md)

The document includes the selection and memory rules, reference pseudocode, conformance tests, timing diagrams, and the historical QST source. Start with Sections 3–10 for behavior, Section 12 for scenarios, or Annex C for worked examples. To check the reference sketch or reuse its timelines in your implementation, see the [reference check guide](tests/README.md).

## Scope and status

The specification defines deterministic keying behavior and accepts two documented same-type re-closure policies; suppression is recommended for software (Section 10.1). It is not presented as an electrically exact reproduction of the 1955 hardware.

Questions, reproducible input timelines and reports of implementation differences are welcome in Issues.

## License and authorship

The specification is licensed under [CC BY 4.0](LICENSE). The historical QST excerpt in Annex A is a separately authored source; the repository license does not relicense that excerpt.

Original document: Paweł (SP5DNA) + Claude AI. Revisions 2026-10-19, 2026-10-20 and 2026-11-01 prepared with Codex following the author's decisions.
