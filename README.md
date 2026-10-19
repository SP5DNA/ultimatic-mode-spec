# Ultimatic Mode Specification

A hardware-independent specification of Ultimatic CW keying for implementers and operators. Ultimatic lets a held paddle remain pressed while the opposite paddle takes control; it does not automatically alternate elements during a squeeze.

**[Read the full specification →](docs/ULTIMATIC_MODE_SPECIFICATION_UNAMBIGUOUS.md)**

**Updated 2026-10-19:** clarified paddle memory and same-type re-closure, corrected timing examples, and added executable conformance checks. [See what changed.](CHANGELOG.md)

The document includes the selection and memory rules, reference pseudocode, conformance tests, timing diagrams, and the historical QST source. Start with Sections 3–10 for behavior, Section 12 for tests, or Annex C for worked examples.

## Scope and status

Revision 2026-10-19 defines a modern, deterministic behavior. Its same-type re-closure policy is an explicit design choice, distinguished from the historical evidence in Section 10.1. It is not presented as an electrically exact reproduction of the 1955 hardware.

Questions, reproducible input timelines and reports of implementation differences are welcome in Issues.

## License and authorship

The specification is licensed under [CC BY 4.0](LICENSE). The historical QST excerpt in Annex A is a separately authored source; the repository license does not relicense that excerpt.

Original document: Paweł (SP5DNA) + Claude AI. Revision 2026-10-19 prepared with Codex following the author's decisions.
