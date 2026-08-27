# Trading Card Break-even Estimator

A configurable expected-value calculator. It does **not** hard-code a platform's current card-drop, fee or regional-tax rules; every rate is an input so the result is transparent and reusable.

```bash
python main.py
pytest -q
```

---

## Live demo

**[Open the live demo](https://mateotrucco.github.io/trading_card_estimator/)**

The demo runs the repository’s original Python logic directly in the browser with Pyodide 314.0.4. The desktop Tkinter interface remains available through `main.py`.

## Repository setup

This separated repository also includes:

- MIT license
- project-specific `.gitignore`
- automated tests / CI
- GitHub Pages deployment for the demo
- `screenshots/` placeholder for portfolio images

The source files from the cleaned portfolio base were preserved unless a web-demo integration file had to be added.

