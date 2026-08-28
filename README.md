# Trading Card Break-even Estimator

A configurable expected-value calculator. It does **not** hard-code a platform's current card-drop, fee or regional-tax rules; every rate is an input so the result is transparent and reusable.

```bash
python main.py
pytest -q
```

---

## Interactive preview

[![Trading Card EV Estimator interface](screenshots/preview.png)](https://mateotrucco.github.io/trading_card_estimator/)

**[Open the live experience](https://mateotrucco.github.io/trading_card_estimator/)** · [View the portfolio](https://mateotrucco.github.io/)

## Engineering baseline

- Business logic separated from presentation
- Automated tests and GitHub Actions CI
- Responsive, keyboard-friendly browser experience
- MIT licensed and documented setup

