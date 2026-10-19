# Changelog

## 2026-10-19

This revision clarifies which paddle presses create stored requests and corrects the worked timing examples. Implementers using the previous reference pseudocode should review Sections 5–10 and update their conformance checks.

- A re-press of the current type during its mark or following space does not queue another element. Repetition requires the paddle to remain held at the next decision. Section 10.1 identifies this as a deliberate modern policy, without claiming electrical equivalence to the 1955 circuit.
- Repeated presses of a type that is already pending coalesce into one request. Earlier outstanding opposite requests retain their order; a later press does not cancel them.
- The reference pseudocode preserves pending order and selects the next mark at the space deadline without an extra update tick.
- Annex C.2 now shows D using a held DIT paddle: DAH 0–470 ms, DIT 300–520 ms, output marks 0–240, 320–400 and 480–560 ms. It demonstrates held squeeze rather than re-closure. C.2b remains the T5 re-closure example.
- Annex C.1 correctly identifies the 200–210 ms press as occurring during DAH. The 250–260 ms press demonstrates input during spacing.
- The historical QST quotation is unchanged. Its relationship to the modern rules is made explicit.
- Added T9–T12 and a check that compiles the C sketch directly from the specification and validates 28 timestamped traces.
- Added reproducible C.1/C.2 diagram sources, with the established dark palette and layout.
- Shortened the README to guide readers to the full specification in `docs`.
