# Timing diagram sources

`draw_c1.py` and `draw_c2.py` recreate the existing dark timing-diagram style from native drawing commands and explicit timestamps. They do not edit an input bitmap. Install the Pillow version in `requirements-diagrams.txt`. Fonts are Arial / Arial Bold and Menlo from macOS; they are not redistributed. C.2 supports `--font-dir` for its Arial files; Menlo is resolved from the macOS system path. On another platform, configure equivalent local fonts in the scripts and inspect the result.

Run from the repository root:

```sh
python3 tools/draw_c1.py
python3 tools/draw_c2.py
python3 -m unittest discover -s tests -v
```

Use `--output /tmp/preview.png` to render without replacing a document image. C.1 renders to 1744 × 3424 px; C.2 to 1708 × 854 px. Both use 2× drawing and LANCZOS downsampling. Palette: background #132c41, panel #153148, DAH #ca811b, DIT #28a99f, text #abcce4, headings #edf4ff.

The unchanged C.2b and C.3 images have no original generator in this repository. These scripts reconstruct C.1/C.2; they are not recovered historical authoring sources.
