# Ultimatic Mode Specification (Unambiguous, Platform-Agnostic)

**Author:** Paweł (SP5DNA)
**Status:** Normative core spec (Sections 1–14) + informative annexes (A–D)

---

## 1. Purpose

This document defines the **Ultimatic keyer behavior** in a deterministic, implementation-independent form.
It is intentionally detached from:
- specific hardware (MCU, GPIO, timers),
- specific programming language,
- specific scheduler architecture (interrupt, polling, RTOS).

The goal is to remove ambiguity in edge cases and provide testable normative behavior.

---

## 2. Normative terms

- **MUST**: required behavior.
- **SHOULD**: recommended behavior.
- **MAY**: optional behavior.

---

## 3. Timing model

Use abstract time units:
- `DIT = 1 unit`
- `DAH = 3 units`
- `INTER_ELEMENT_SPACE = 1 unit`

Character/word spacing is outside core Ultimatic element selection logic and may be handled by higher-level text/keying layer.

A worked reference example at a concrete speed (15 WPM, 80 ms dit unit) is given in **Annex C** for illustration only; it is not itself normative — conformance is judged against Sections 5–11.

---

## 4. Inputs and events

Two paddles:
- `DIT_PADDLE`
- `DAH_PADDLE`

Each paddle has:
- level (`pressed` / `released`)
- rising-edge event (`released -> pressed`)

Core Ultimatic decisions are based on:
1. current paddle levels,
2. rising-edge memory flags,
3. last-touch ordering.

---

## 5. Core guarantees

1. **Edge guarantee**
   Every rising edge on a paddle MUST guarantee at least one element of that paddle type.

2. **Continuous generation**
   Holding a paddle MAY produce repeated elements of that type.

3. **Order fidelity**
   If opposite paddle is pressed before next element decision, ordering MUST respect closure order using memory semantics.

4. **No mid-element preemption**
   Once an element starts, it MUST complete before switching type.

---

## 6. Abstract state

Maintain:
- `dit_memory` (bool)
- `dah_memory` (bool)
- `last_touched` in `{DIT, DAH, NONE}`
- `state` in `{IDLE, SENDING_DIT, SENDING_DAH, SPACING}`

Memory flags are set on rising edges and consumed when a new element starts.

`last_touched` MUST be updated on **every** rising edge, regardless of which paddle started the character and regardless of whether the other paddle is currently held. It is not a "which paddle opened this character" flag — it is a live pointer to the most recent edge. (This distinction is what Section 8 Priority 1/3 and Annex B depend on; a static "first paddle of the character" substitute does not satisfy RQ-equivalent behavior and fails the flick-the-first-paddle case in Annex C/T8.)

---

## 7. Rising-edge processing (normative)

On each input update:

1. If `DIT` rising edge:
   2. set `dit_memory = true`
   3. set `last_touched = DIT`

2. If `DAH` rising edge:
   2. set `dah_memory = true`
   3. set `last_touched = DAH`

If both rising edges are observed in the same update instant, implementation MUST define deterministic tie-break:
- preferred: preserve true chronological order if available,
- otherwise use fixed policy and document it.

---

## 8. Element selection at IDLE (normative priority)

When state enters `IDLE`, select next element by strict priority:

### Priority 1: both memories set
If `dit_memory && dah_memory`:
- choose by `last_touched`:
  - `last_touched == DIT` -\> send `DIT`
  - `last_touched == DAH` -\> send `DAH`
- clear only the consumed memory flag.

### Priority 2: single memory set
- if only `dit_memory`: send `DIT`, clear `dit_memory`
- if only `dah_memory`: send `DAH`, clear `dah_memory`

### Priority 3: no memory, both paddles held
If both levels are pressed:
- choose by `last_touched` (same as above).

### Priority 4: no memory, one paddle held
- only DIT pressed -\> send DIT
- only DAH pressed -\> send DAH

### Priority 5: no request
If no memory and no paddle held: remain IDLE.

---

## 9. Transmission state behavior

1. `SENDING_DIT`
   2. key output ON for exactly `1 unit`
   3. then go to `SPACING`

2. `SENDING_DAH`
   2. key output ON for exactly `3 units`
   3. then go to `SPACING`

3. `SPACING`
   2. key output OFF for exactly `1 unit`
   3. then go to `IDLE` and run selection rules again

Memory updates from rising edges MUST still be accepted during sending and spacing; they apply to subsequent element selection.

---

## 10. Re-closure behavior

If a paddle is released and pressed again, that new rising edge MUST create a new memory request, even if the same paddle was active previously.

This ensures "flick/reclosure seizes control for at least one element" — **symmetrically for either paddle**, including the paddle that opened the character, even while the other paddle is held continuously (QST 1955 point 6; see Annex A and T8). An implementation that only re-evaluates control when the *second* paddle is released (and never re-arms control for the *first* paddle while the second stays down) does not satisfy this section.

---

## 11. Determinism requirements

An implementation is conformant only if:

1. Same input event timeline always produces same output timeline.
2. Selection priority is exactly as specified.
3. Memory consumption happens at element start (not at element end).
4. No element is truncated by opposite-paddle activity.

---

## 12. Conformance test scenarios (minimum)

### T1: Single tap
- Tap DIT once -\> exactly one DIT
- Tap DAH once -\> exactly one DAH

### T2: Hold repeat
- Hold DIT -\> repeated DIT elements separated by 1-unit spacing
- Hold DAH -\> repeated DAH elements separated by 1-unit spacing

### T3: Seizure during opposite element
- Start DAH, press DIT before next IDLE decision -\> next element becomes DIT
- Worked trace: Annex C, Letter N, Scenarios 1–5.

### T4: Squeeze with maintained first paddle
- Hold first paddle continuously, tap second -\> alternation according to closure order

### T5: Re-closure of the second (squeeze) paddle
- Hold first paddle, press/release/re-press the second paddle rapidly -\> each rising edge yields at least one guaranteed element
- Worked trace: Annex C, Letter D re-closure example.

### T6: Both memories set at decision
- Force both memories true before IDLE decision -\> winner MUST follow `last_touched`

### T7: Press during spacing
- Opposite paddle press during spacing MUST affect next element decision.

### T8: Re-closure of the *first* paddle while the second is held continuously (critical, easily missed)
- Hold paddle A (opens the character). Squeeze paddle B and hold it continuously (control transfers to B per T4).
- While B is still held down without interruption, release and re-press A (a flick).
- Expected: A's rising edge sets `last_touched = A` and `A_memory = true`; per Section 8 Priority 1, control MUST return to A for at least one element, even though B never stopped being held, and even though A already sent an element earlier in this same character.
- This is the asymmetric counterpart of T5. An implementation that tracks only "which paddle opened the character" (a static flag) instead of a live `last_touched` will pass T4/T5 but **fail T8**, because it never re-arms while the other paddle stays down. This exact failure mode has been found in real-world Ultimatic implementations during spec-conformance review, which is why it is called out here explicitly.

---

## 13. Out-of-scope (explicit)

This specification does **not** define:
- WPM storage/UI/menu behavior,
- message memories/macros,
- battery/sleep policy,
- sidetone frequency generation,
- radio interface electronics.

Those are higher-layer features and must not alter core Ultimatic selection semantics.

---

## 14. Reference execution sketch (language-neutral)

At each engine update:

1. read input levels
2. detect rising edges, update memory + last\_touched
3. if `state == IDLE`, run priority selection and possibly start new element
4. if sending state elapsed, transition to SPACING or IDLE per timing rules
5. repeat

Any architecture (tick-based, event-driven, hybrid) is valid if observable behavior matches Sections 7–12.

A fully worked, compilable-style pseudocode implementing this sketch (correctly, including `last_touched`) is given in **Annex B**.

---
---

# Annex A — Original source text (informative)

Primary source: **QST Magazine, May 1955**, "Summary of Actions of the Keys."
Scanned original available at: [https://www.worldradiohistory.com/Archive-DX/QST/50s/QST-1955-05.pdf][1]
Reproduced here for traceability, since every normative requirement in Sections 5–11 is a direct restatement of one of these seven points.

1. A single character is generated by momentary or prolonged closure of a key. The character is held by the memory for a positive time-base pulse if the key is released prior to that pulse.

2. Successive like characters are generated by constant closure of a key.

3. When one memory is already actuated, closure of the opposite key before generation of the first-stored character activates the opposite memory. The firstly actuated memory retains control of the sequencer until one character of its type is delivered at the output. The secondly actuated memory then assumes control of the sequencer (as the first key is open or still closed) and the next output character is of the second type.

4. Continued closure of this second key maintains control of the sequencer after the transfer action, and the output is a series of the second type until that key is released. This obtains even with the first key still closed.

5. Release of the second key, with the first key still closed, causes the output to revert to the first character type.

6. Release and reclosure of the first key (just a flick!) reactuates the first memory and seizes control of the sequencer — the second key closed all the while — and the output reverts to the first character type until that first key is again released or until the opposite type character is flicked in by the second key. At least one character of the first type is guaranteed by the memory.

7. In recapitulation, any closure of a key guarantees at least one character of that type, transmitted in correct relationship to the order of closure, regardless of intervening selective motions. Whenever a key makes contact, the output subsequent to the character in progress corresponds to that key until the other key makes contact or the first key is released.

**Mapping to this spec:** Point 1 → §5.1/§7. Point 2 → §5.2/§8 Priority 4. Point 3 → §5.3/§8 Priority 1–2. Point 4 → §8 Priority 3/§9. Point 5 → §8 Priority 4 (falls through once the seizing paddle's memory/level clears). Point 6 → §10 and **T8** — this is the point that is easiest to under-implement, because a naive reading of point 3 ("firstly actuated memory") tempts an implementer into a *static* first-paddle flag rather than a *live* `last_touched` pointer. Point 7 → §5, general guarantee.

---

# Annex B — Reference pseudocode (informative, non-normative)

This is a corrected, complete reference implementation of Sections 6–9, written to make `last_touched` explicit and live (unlike a "first paddle of the character" flag, which satisfies T1–T7 but fails T8).

```c
// --- Abstract state (Section 6) ---
bool dit_memory = false, dah_memory = false;

typedef enum { NONE, DIT, DAH } Paddle;
Paddle last_touched = NONE;

typedef enum { IDLE, SENDING_DIT, SENDING_DAH, SPACING } State;
State state = IDLE;
uint32_t units_remaining = 0;

bool prev_dit = false, prev_dah = false;

static void start_element(State s, uint32_t units, bool *memory_to_clear) {
    key_down();
    state = s;
    units_remaining = units;
    if (memory_to_clear) *memory_to_clear = false;   // Section 6: cleared at START, not end
}

// Called once per engine update (tick or event) with current paddle levels.
void ultimatic_update(bool dit_paddle, bool dah_paddle) {

    // --- Section 7: rising-edge processing ---
    bool dit_edge = dit_paddle && !prev_dit;
    bool dah_edge = dah_paddle && !prev_dah;

    if (dit_edge && dah_edge) {
        // Section 7 tie-break: simultaneous edges observed in the same update.
        // Fixed, documented policy (adjust if your platform can resolve true
        // chronological order, e.g. via interrupt timestamps): DAH wins last_touched.
        dit_memory = true;
        dah_memory = true;
        last_touched = DAH;
    } else if (dit_edge) {
        dit_memory = true;
        last_touched = DIT;                 // <-- updated on EVERY dit edge, even a
                                              //     flick of the paddle that opened
                                              //     the character (needed for T8)
    } else if (dah_edge) {
        dah_memory = true;
        last_touched = DAH;                 // <-- symmetric for dah
    }

    // --- state machine ---
    switch (state) {

    case IDLE:
        // Section 8: strict priority selection
        if (dit_memory && dah_memory) {                    // Priority 1
            if (last_touched == DIT) start_element(SENDING_DIT, 1, &dit_memory);
            else                     start_element(SENDING_DAH, 3, &dah_memory);
        } else if (dit_memory) {                             // Priority 2
            start_element(SENDING_DIT, 1, &dit_memory);
        } else if (dah_memory) {
            start_element(SENDING_DAH, 3, &dah_memory);
        } else if (dit_paddle && dah_paddle) {                // Priority 3
            if (last_touched == DIT) start_element(SENDING_DIT, 1, NULL);
            else                     start_element(SENDING_DAH, 3, NULL);
        } else if (dit_paddle) {                              // Priority 4
            start_element(SENDING_DIT, 1, NULL);
        } else if (dah_paddle) {
            start_element(SENDING_DAH, 3, NULL);
        }
        // else Priority 5: remain IDLE
        break;

    case SENDING_DIT:
    case SENDING_DAH:
        if (--units_remaining == 0) {
            key_up();
            state = SPACING;
            units_remaining = 1;
        }
        break;

    case SPACING:
        if (--units_remaining == 0) {
            state = IDLE;                    // next update re-runs Section 8 selection
        }
        break;
    }

    prev_dit = dit_paddle;
    prev_dah = dah_paddle;
}
```


---

# Annex C — Worked timing example (informative)

Reference speed for this annex only: **15 WPM**, dit unit = 80 ms, dah = 240 ms, element space = 80 ms. This is illustrative; the normative spec (Sections 3, 9) uses abstract units so any speed applies identically.

### C.1 — Letter N (`- ·`), T3 / T7 worked

Five input timelines, all conformant, all producing **DAH (0–240 ms), SPACE (240–320 ms), DIT (320–400 ms)**:

| Scenario | DAH paddle | DIT paddle | Note                                                |
| -------- | ---------- | ---------- | --------------------------------------------------- |
| 1        | 0–160 ms   | 10–80 ms   | plain squeeze during DAH                            |
| 2        | 0–160 ms   | 200–210 ms | squeeze arrives **during SPACE** (T7)               |
| 3        | 0–340 ms   | 250–260 ms | DAH held past its own element into the space        |
| 4        | 0–420 ms   | 300–410 ms | DAH held through the whole character                |
| 5        | 0–430 ms   | 300–470 ms | DAH held through character + partial trailing space |

![Annex C.1 timing diagram — five conformant DAH/DIT paddle timelines for letter N, all converging on the same DAH–space–DIT output][image-1]

*Figure C.1 — the DAH rising edge at 0 ms always wins the first element; the DIT rising edge only needs to land before the IDLE decision at 320 ms (dashed line), and MAY occur during `SPACING` (scenario 2). Scenarios 3–5 hold DAH well past its own element for illustration only — memory is consumed at element start, not release, so the extra hold changes nothing.*

Takeaway: the DIT rising edge only needs to land before the IDLE decision that follows the DAH+space (i.e. before 320 ms); exactly *when* within that window is irrelevant, and it MAY occur during `SPACING` (Section 9's requirement that memory updates are accepted during spacing).

### C.2 — Letter D (`-··`), T5 re-closure of the second paddle

| Paddle | Timeline                                               |
| ------ | ------------------------------------------------------ |
| DAH    | held 0–470 ms                                          |
| DIT    | pressed 300–340 ms, released, pressed again 380–420 ms |

![Annex C.2 timing diagram — DAH held continuously while DIT is pressed twice, each press independently guaranteeing its own element][image-2]

Result: **DAH (0–240), SPACE, DIT (320–400), SPACE, DIT (400... next cycle)** → decoded as **D** (`-··`).

Each DIT rising edge (at 300 ms and again at 380 ms) independently sets `dit_memory` and guarantees its own element — this is the Section 5/T5 edge guarantee applied twice in one character. (An earlier draft of this example mislabeled the result as "`--`"; the correct decode is `-··` = D, matching the two independently-guaranteed DIT elements.)

### C.3 — T8 worked trace (the case that is easy to get wrong)

| Paddle                              | Timeline                                             |
| ----------------------------------- | ---------------------------------------------------- |
| DAH (paddle A, opens the character) | 0–160 ms, released, **380–460 ms** (reclosure)       |
| DIT (paddle B)                      | 100 ms onward, **held continuously, never released** |

Expected per Section 8/10 and T8:
1. `0 ms`: DAH edge → `dah_memory=true`, `last_touched=DAH` → sends DAH (0–240 ms).
2. `100 ms`: DIT edge arrives mid-DAH → `dit_memory=true`, `last_touched=DIT`. Captured per Section 9 (accepted during sending).
3. `240–320 ms`: SPACING, then IDLE decision: `dah_memory` was already cleared when the DAH element started in step 1, so only `dit_memory` is set → Priority 2 → sends DIT (320–400 ms). Control has transferred to B, matching point 3/4.
4. DIT paddle never releases, so absent a new edge, further IDLE decisions keep selecting DIT (Priority 4, single paddle held) — B keeps control, matching point 4.
5. `380 ms`: DAH paddle (A) is re-closed — **while B is still held**. This is a fresh rising edge: `dah_memory=true`, `last_touched=DAH`.
6. `400–480 ms`: SPACING, then at the next IDLE decision (480 ms): `dit_memory` was cleared when the DIT element started at 320 ms, so only `dah_memory` is set (from the edge at 380 ms) → Priority 2 → sends **DAH** (480–720 ms), even though B (DIT) never stopped being held — and even though A itself had already released by 460 ms. The guarantee fires purely off the memory flag, not the paddle levels.
7. Control stays with DAH only for the guaranteed element sent in step 6; once `dah_memory` is consumed at its start (480 ms) and no new A edge has occurred, the next IDLE decision (800 ms) has no memory at all. Paddle A is not held (it released at 460 ms) but paddle B still is → Priority 4 → control reverts to B, which keeps sending DIT for as long as it stays held with no new edge.

![Annex C.3 timing diagram — paddle A flicked again at 380 ms while paddle B stays held, forcing a guaranteed DAH reseize before control reverts to B][image-3]

---

# Annex D — Implementation checklist (informative)

- [ ] Rising-edge detection for both paddles, independent of debounce/polling strategy.
- [ ] `dit_memory` / `dah_memory` flags that persist across state transitions (KEY\_START/KEYED/SPACING or equivalent).
- [ ] `last_touched` is a **live** pointer updated on every rising edge — not a "which paddle opened this character" flag that only resets when both paddles release.
- [ ] IDLE priority implemented in the exact order of Section 8 (both-memory → single-memory → both-held → single-held → none).
- [ ] Memory flag cleared at element **start**, not element end.
- [ ] Element duration is fixed (1 unit DIT / 3 units DAH) and is never truncated by opposite-paddle activity.
- [ ] Rising edges arriving during `SENDING_*` or `SPACING` are captured and influence the next IDLE decision (Section 9).
- [ ] Re-closure works symmetrically for **either** paddle, including the paddle that opened the character, while the other paddle is held continuously (T8) — not just re-closure of the "second"/squeeze paddle (T5).
- [ ] Simultaneous-edge tie-break is deterministic and documented (Section 7).
- [ ] Tested against T1–T8 (Section 12), including T8 specifically, before calling the mode conformant.

[1]:	https://www.worldradiohistory.com/Archive-DX/QST/50s/QST-1955-05.pdf

[image-1]:	annex-c1-timing-diagram.png
[image-2]:	annex-c2-timing-diagram.png
[image-3]:	annex-c3-timing-diagram.png