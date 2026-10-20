# Changelog

## 2026-10-20

Both current-type re-closure policies are now acceptable. Implementers MUST document whether a new same-type press during the current mark or its following space is remembered or suppressed. This replaces the suppression-only requirement of the 2026-10-19 revision.

- Retained the held-squeeze D example C.2, which works under both policies. Restored its earlier two-DIT-tap timeline as C.2a, with a diagram for the remembered variant and explicit D versus N results for the two policies.
- Analysis of the QST description and schematic suggests the original circuit most likely remembered same-type re-closure after memory clearance at mark start. This remains an inference, without electrical simulation or original-hardware measurement.
- Suppression remains accepted to limit surprise for operators accustomed to this behavior in common Iambic A/B implementations. The difference has limited significance in typical squeeze use but can change a release-and-repress sequence.
- Added an explicit policy choice to the reference sketch; the default remains suppression. Updated T9/T11 and the reference checks to exercise both policies, mirrored DIT/DAH cases, coalescing and pending-request order.
- Opposite-type memory, one pending request per type, timing, squeeze takeover and return remain common requirements. The historical quotation is unchanged. Diagram-generation tools remain in the author's local archive.

## 2026-10-19

This revision clarifies which paddle presses create stored requests and corrects the worked timing examples. Implementers using the previous reference pseudocode should review Sections 5–10 and update their conformance checks.

- A re-press of the current type during its mark or following space does not queue another element. Repetition requires the paddle to remain held at the next decision. Section 10.1 identifies this as a deliberate modern policy, without claiming electrical equivalence to the 1955 circuit.
- Repeated presses of a type that is already pending coalesce into one request. Earlier outstanding opposite requests retain their order; a later press does not cancel them.
- The reference pseudocode preserves pending order and selects the next mark at the space deadline without an extra update tick.
- Annex C.2 now shows D using a held DIT paddle: DAH 0–470 ms, DIT 300–520 ms, output marks 0–240, 320–400 and 480–560 ms. It demonstrates held squeeze rather than re-closure. C.2b remains the T5 re-closure example.
- Annex C.1 correctly identifies the 200–210 ms press as occurring during DAH. The 250–260 ms press demonstrates input during spacing.
- The historical QST quotation is unchanged. Its relationship to the modern rules is made explicit.
- Added T9–T12 and a check that compiles the C sketch directly from the specification and validates 28 timestamped traces.
- Corrected C.1/C.2 diagrams while retaining the established dark palette and layout. Diagram-generation tools are maintained separately in the author's local archive.
- Shortened the README to guide readers to the full specification in `docs`.

- Documented how implementers can run the reference checks and adapt the timelines to their own firmware, including the limits of a passing result.
