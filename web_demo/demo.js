import { bootPython, parsePythonJson } from './pyodide-helper.js';

let py;
const ids = ['cards', 'drop', 'sale', 'price', 'tax', 'fee'];
const out = document.querySelector('#output');
const run = document.querySelector('#run');
const presets = {
  cautious: [6, 35, 0.12, 0.80, 10, 8],
  optimistic: [12, 60, 0.28, 0.65, 5, 5],
  'thin-margin': [8, 45, 0.18, 0.60, 12, 10],
};

async function init() { py = await bootPython(['estimator.py']); run.disabled = false; calc(); }

function calc() {
  if (!py) return;
  for (const id of ids) py.globals.set(id, document.querySelector(`#${id}`).value);
  try {
    const raw = py.runPython(`import json\nfrom estimator import break_even_sale_price, estimate_break_even, roi_percent\nr=estimate_break_even(cards,drop,sale,price,tax,fee)\nb=break_even_sale_price(cards,drop,price,tax,fee)\nroi=roi_percent(r)\njson.dumps({**{k:str(getattr(r,k)) for k in ('expected_cards','gross_revenue','marketplace_fees','net_revenue','purchase_total','profit')},'break_even':str(b) if b is not None else None,'roi':str(roi) if roi is not None else None})`);
    const data = parsePythonJson(raw);
    const profitable = Number(data.profit) >= 0;
    document.querySelector('#estimateMetrics').innerHTML = `<div class="metric"><strong>${data.expected_cards}</strong><small>Expected cards</small></div><div class="metric"><strong>${data.net_revenue}</strong><small>Net revenue</small></div><div class="metric"><strong>${data.profit}</strong><small>Profit / loss</small></div><div class="metric"><strong>${data.roi ?? '—'}${data.roi ? '%' : ''}</strong><small>ROI</small></div>`;
    const roiWidth = Math.max(0, Math.min(100, 50 + Number(data.roi || 0) / 2));
    document.querySelector('#roiMeter').style.width = `${roiWidth}%`;
    out.textContent = `${profitable ? 'Positive' : 'Negative'} expected-value scenario\nBreak-even average sale price: ${data.break_even ?? 'Unavailable'}\nGross revenue: ${data.gross_revenue}\nMarketplace fees: ${data.marketplace_fees}\nPurchase total: ${data.purchase_total}\n\nThis is a transparent scenario model, not a prediction or financial recommendation.`;
  } catch (error) {
    out.textContent = `Validation error: ${error.message}`;
  }
}

for (const input of ids.map((id) => document.querySelector(`#${id}`))) input.addEventListener('input', calc);
for (const button of document.querySelectorAll('[data-preset]')) button.addEventListener('click', () => {
  presets[button.dataset.preset].forEach((value, index) => { document.querySelector(`#${ids[index]}`).value = value; });
  calc();
});
run.disabled = true;
run.addEventListener('click', calc);
init().catch(() => {});
