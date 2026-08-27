import {bootPython,parsePythonJson} from './pyodide-helper.js';let py;const ids=['cards','drop','sale','price','tax','fee'],out=document.querySelector('#output'),run=document.querySelector('#run');async function init(){py=await bootPython(['estimator.py']);run.disabled=false;calc();}function calc(){if(!py)return;for(const id of ids)py.globals.set(id,document.querySelector('#'+id).value);try{const raw=py.runPython(`import json
from estimator import estimate_break_even
r=estimate_break_even(cards,drop,sale,price,tax,fee)
json.dumps({k:str(getattr(r,k)) for k in ('expected_cards','gross_revenue','marketplace_fees','net_revenue','purchase_total','profit')})`);const d=parsePythonJson(raw);out.textContent=`Expected cards: ${d.expected_cards}
Gross revenue: ${d.gross_revenue}
Marketplace fees: ${d.marketplace_fees}
Net revenue: ${d.net_revenue}
Purchase total: ${d.purchase_total}
Profit / loss: ${d.profit}`;}catch(e){out.textContent='Error: '+e.message;}}run.disabled=true;run.addEventListener('click',calc);init().catch(()=>{});
