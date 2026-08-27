"""GUI for the configurable trading-card break-even estimator."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from estimator import estimate_break_even


class TradingCardEstimator(tk.Tk):
    FIELDS = (
        ("Total cards in set", "10"),
        ("Expected drop rate (%)", "50"),
        ("Average sale price", "0.10"),
        ("Game price", "0.50"),
        ("Purchase tax (%)", "0"),
        ("Marketplace fee (%)", "0"),
    )

    def __init__(self) -> None:
        super().__init__()
        self.title("Trading Card Break-even Estimator")
        self.geometry("720x470")
        self.minsize(620, 430)
        self.inputs: list[tk.StringVar] = []
        self.result = tk.StringVar(value="Enter your own rates; no platform rules are assumed.")
        self._build()

    def _build(self) -> None:
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="Trading Card Break-even Estimator", font=("TkDefaultFont", 18, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 18))
        for row, (label, default) in enumerate(self.FIELDS, start=1):
            value = tk.StringVar(value=default)
            self.inputs.append(value)
            ttk.Label(frame, text=label).grid(row=row, column=0, sticky="w", padx=(0, 20), pady=5)
            ttk.Entry(frame, textvariable=value).grid(row=row, column=1, sticky="ew", pady=5)
        ttk.Button(frame, text="Calculate", command=self.calculate).grid(row=7, column=1, sticky="e", pady=16)
        ttk.Separator(frame).grid(row=8, column=0, columnspan=2, sticky="ew", pady=(0, 12))
        ttk.Label(frame, textvariable=self.result, justify="left", wraplength=650).grid(row=9, column=0, columnspan=2, sticky="w")
        frame.columnconfigure(1, weight=1)

    def calculate(self) -> None:
        try:
            result = estimate_break_even(*(value.get() for value in self.inputs))
        except ValueError as exc:
            messagebox.showerror("Invalid input", str(exc))
            return
        outcome = "estimated profit" if result.profit >= 0 else "estimated loss"
        self.result.set(
            f"Expected cards: {result.expected_cards}\n"
            f"Gross revenue: {result.gross_revenue}\n"
            f"Marketplace fees: {result.marketplace_fees}\n"
            f"Net revenue: {result.net_revenue}\n"
            f"Purchase total: {result.purchase_total}\n"
            f"{outcome.title()}: {abs(result.profit)}"
        )


if __name__ == "__main__":
    TradingCardEstimator().mainloop()
