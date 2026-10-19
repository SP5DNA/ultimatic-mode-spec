# Reference checks for implementers

`test_reference.py` checks that the C-style reference sketch in Annex B produces the output timelines required by this specification. It is an executable companion to Section 12 and Annex C, intended to help developers implement Ultimatic in their own devices.

## Run the checks

From the repository root:

```sh
python3 -m unittest discover -s tests -v
```

Requirements:

- Python 3, using only its standard library; no Python packages to install.
- A C compiler supporting C11 and the GCC/Clang command-line options used by the script. The check can run on a development computer; an MCU, paddles and a radio are not required.
- `CC` can name a compiler executable. If it is unset, the script looks for `cc`, then `clang` on PATH.

For example, select Clang explicitly with:

```sh
CC=clang python3 -m unittest discover -s tests -v
```

The script compiles and runs a temporary host program. It does not transmit RF, connect to hardware or edit the specification. Temporary compilation files are removed afterwards.

A successful run reports `OK` and:

```text
Validated 28 timestamped traces against the embedded C sketch.
```

Python's runner reports one test method: that method checks 28 timelines. This does not mean there are 28 separate unittest methods. A compilation failure, missing compiler, runtime assertion or mismatching timeline makes the check fail. For timeline mismatches, the output identifies the scenario and shows the actual and expected marks.

## What is exercised

The script extracts the first C code block from the main specification, currently the reference sketch in Annex B. It adds input and output stubs, compiles that extracted code, and records the type, start and end of each mark.

The 28 timelines cover single taps, held repetition, opposite-type memory during marks and spaces, current-type re-closure suppression, held input at the next decision, coalescing repeated requests, squeeze takeover and return, the C.1/C.2/C.2b/C.3 examples, selected mirrored cases, exact-boundary presses and releases, and both orders of two pending types. The two pending-order checks directly prepare internal pending state; they are not hardware-input recordings.

The test harness advances a simulated clock in 1 ms steps and supplies logical paddle levels at each step. This is a deterministic test setup, not a requirement that production firmware poll at 1 ms intervals. It reaches every phase deadline in the example sketch, whose unit is 80 ms (15 WPM).

## Use the timelines for your implementation

1. Read the normative rules in Sections 3–11, especially the modern memory policy in Section 10.1.
2. Reproduce the input intervals from the `cases` list in a test adapter for your firmware or simulator. An interval `(start, end)` is pressed at `start` and released at `end`; the end is excluded.
3. Record output marks as `(type, start, end)` and compare with the listed expected marks. Adjust all timestamps consistently if using another unit duration.
4. Add tests for your input filtering, timer resolution, interrupt or polling architecture, and hardware output separately.

For example, the `C2 D` case holds DAH during `[0, 470)` ms and DIT during `[300, 520)` ms. Expected marks are DAH `[0, 240)`, DIT `[320, 400)` and DIT `[480, 560)` ms. Gaps follow from the end of one mark and the start of the next.

Running this script unchanged tests only the embedded reference sketch. It does not automatically test a separate firmware implementation. Reuse of its input/output cases requires an adapter, and its internal-state checks require an equivalent state setup or a separately designed integration test.

## What a passing result does not establish

The expected timelines encode the rules adopted in this specification. Therefore the check establishes agreement between that sketch and those expected examples; it is not independent evidence that the selected rules reproduce the original 1955 Ultimatic circuit.

It is not an exhaustive proof of correctness or certification of conformance. It does not cover every possible input sequence, every timing scale, physical 1 ms pulse detection, contact bounce, electrical behavior, timer jitter, RF output, or the behavior of any particular commercial keyer. It does not replace the normative requirements or testing on your target device.

To propose a new case, supply timestamped paddle closures, expected marks, and the relevant specification rule. A disagreement about an expected result should be resolved against the rules first; changing the expected output merely to make the test pass would defeat its purpose.
