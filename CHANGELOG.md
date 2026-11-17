# Revision history

## 2026-11-17

**Breaking clarification: same-type re-closure memory ("remember current type") and example C.2a have been removed.**

A press of the type currently being sent, during its mark or following space, now always produces no stored request (Section 10.1). There is no longer a choice of policy, no configuration option and no declaration requirement. This is the behaviour the reference code already used by default ("suppress current type").

Why: revisions 2026-10-20 and 2026-11-01 documented the "remember" variant and example C.2a (two DIT taps giving D) because the circuit described in QST, May 1955, probably behaved that way. That was an inference, never confirmed on hardware, and the behaviour adds nothing to Ultimatic operation: elements are repeated by holding a paddle (C.2). Keeping it as an accepted option was misleading to implementers.

Changes: removed the policy table, the "remember" variant, Annex C.2a and its diagram, the policy selector from the Annex B code, and all policy-dependent checks. T9 now includes the two-tap timeline, whose required output is N. Opposite-type memory (T3, T5, T7, T8) is unchanged. Implementations that added the "remember" variant should remove it. The test harness now also builds with GCC.

## 2026-11-01

*Superseded by 2026-11-17.* Clarified C.2a as an informative historical example and recommended current-type re-closure suppression for software implementations. Both variants remain accepted. No changes to the reference code or timing diagrams.

## 2026-10-20

*Superseded by 2026-11-17.* Accepted both current-type re-closure policies, requiring implementations to document their choice. Added the two-tap example C.2a, a policy selector in the reference code, and checks for both variants. The reference default remains suppression.

## 2026-10-19

Specified pending-request order, coalescing and exact element-boundary timing. Updated the reference code and timing examples, and added executable reference checks. Implementations based on earlier revisions should review Sections 5–10.
