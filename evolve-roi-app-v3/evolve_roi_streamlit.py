
import streamlit as st
import pandas as pd
import math
from pathlib import Path
import base64

st.set_page_config(page_title="Evolve® HDD Tractor ROI", layout="wide")

# ---- THEME OVERRIDE (dark green) ----
st.markdown("""
<style>
:root { --bg:#064e3b; --card:#065f46; --border:#047857; --text:#ecfdf5; --muted:#a7f3d0; --accent:#10b981; }
html, body, [data-testid="stAppViewContainer"] { background: var(--bg); color: var(--text); }
[data-testid="stSidebar"] { background: var(--card); }
.block-container { padding-top: 1rem; }
hr { border-color: var(--border); }
div[data-testid="stMetricValue"], div[data-testid="stMetric"] { color: var(--text) !important; }
.stButton>button { background: var(--accent); color:#062; border-radius:12px; border: 0; font-weight:600; }
.stDownloadButton>button { background: #ecfdf5; color:#064e3b; border-radius:12px; border: 0; font-weight:600; }
input, .stNumberInput input { background:#064e3b; color:var(--text); border:1px solid var(--border); }
</style>
""", unsafe_allow_html=True)

# ---- Robust logo loader ----
def show_logo():
    here = Path(__file__).parent
    candidates = [here / "logo.png", here.parent / "logo.png"]
    img_bytes = None
    for p in candidates:
        if p.exists():
            img_bytes = p.read_bytes()
            break
    if img_bytes is None:
        # Fallback to embedded image
        img_bytes = base64.b64decode("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")
    st.image(img_bytes, use_column_width=True)

cols = st.columns([1,4,2])
with cols[0]:
    show_logo()
with cols[1]:
    st.title("Evolve® HDD Tractor ROI Calculator")
with cols[2]:
    st.write("")
    st.caption("Dark Green Edition + Report Export")

with st.sidebar:
    st.header("Load from Excel (optional)")
    uploaded = st.file_uploader("Upload 'Evolve ROI Calculator HDD Tractor.xlsx'", type=["xlsx"])
    st.caption("If provided, the app will try to read example defaults from the 'Evolve® ROI Data Input Page'.")

# --- Helpers ---
def coalesce_num(x, default):
    try:
        if x is None or (isinstance(x, float) and math.isnan(x)):
            return default
        return float(x)
    except Exception:
        return default

def try_extract_defaults_from_excel(file):
    try:
        xl = pd.read_excel(file, sheet_name="Evolve® ROI Data Input Page", header=None)
        label_to_value = {}
        for i in range(min(120, len(xl))):
            row = xl.iloc[i].tolist()
            for j, v in enumerate(row):
                if isinstance(v, str) and v.strip():
                    for k in range(1, 4):
                        if j+k < len(row):
                            nxt = row[j+k]
                            if isinstance(nxt, (int, float)) and not pd.isna(nxt):
                                label_to_value[v.strip()] = float(nxt)
                                break
        defaults = {
            "miles": 100000,
            "costQuartEvolve": coalesce_num(label_to_value.get("Modeled Cost / Qrt of Evolve® Oil "), 19.5),
            "costQuartIncumbent": coalesce_num(label_to_value.get("Modeled Cost / Qrt. of Incumbent Oil"), 3.85),
            "costDiesel": coalesce_num(label_to_value.get("Modeled Cost For 1 Gallon of Diesel Fuel"), 4.63),
            "costDEF": coalesce_num(label_to_value.get("Modeled Cost For 1 Gallon of DEF"), 6.0),
            "costOilFilter": coalesce_num(label_to_value.get("Modeled Replacement cost of 1 new Oil Filter"), 0.0),
            "laborRate": coalesce_num(label_to_value.get("Modeled Fully Loaded Labor Cost / Hour"), 75.0),
            "quartsPerODI": coalesce_num(label_to_value.get("Quarts of oil used Per Oil Drain Interval (ODI)"), 10),
            "odiMiles": coalesce_num(label_to_value.get(" Oil Drain Interval [ODI] Miles"), 10000),
            "odiMultiplierX": coalesce_num(label_to_value.get('Expected New Lubricant Multiplier for "Extended" ODI or DPF Service Intervals'), 1.5),
            "laborHoursPerODI": coalesce_num(label_to_value.get("Labor Hours Required for 1 ODI"), 1.0),
            "currentMPG": coalesce_num(label_to_value.get("Current MPG"), 12.0),
            "mpgIncreasePct": coalesce_num(label_to_value.get("Modeled % MPG Increase using New Lubricant"), 5.0),
            "defGalPer100Fuel": coalesce_num(label_to_value.get("DEF Gallons used / 100 Gallons of Fuel"), 3.0),
            "defReductionPct": coalesce_num(label_to_value.get("Modeled DEF Reduction % using New Lubricant"), 10.0),
            "dpfIntervalMiles": coalesce_num(label_to_value.get("Current DPF Service Interval"), 350000),
            "dpfMultiplierX": coalesce_num(label_to_value.get("New Lubricant DPF Service Interval (Calculated off #10 & #16 inputs.)"), 1.5),
            "dpfLaborHours": coalesce_num(label_to_value.get("Labor Hrs Required to Clean or Replace 1 DPF Filter"), 2.0),
            "dpfRefurbishCost": coalesce_num(label_to_value.get("Cost of a Clean / Refurbished DPF Filter (w/o labor)"), 1500),
            "dpfReplaceCost": coalesce_num(label_to_value.get("Cost of a New Replacement DPF Filter (w/o labor)"), 4000),
        }
        return defaults
    except Exception:
        return None

excel_defaults = try_extract_defaults_from_excel(uploaded) if uploaded else None

# --- INPUTS ---
st.subheader("Inputs")

colA, colB, colC = st.columns(3)

with colA:
    miles = st.number_input("Miles traveled (per tractor)", value=100000 if not excel_defaults else int(excel_defaults["miles"]), step=1000, min_value=0)
    costQuartEvolve = st.number_input("Cost / quart – Evolve®", value=19.5 if not excel_defaults else excel_defaults["costQuartEvolve"], min_value=0.0)
    costQuartIncumbent = st.number_input("Cost / quart – Incumbent", value=3.85 if not excel_defaults else excel_defaults["costQuartIncumbent"], min_value=0.0)
    costDiesel = st.number_input("Diesel cost / gallon", value=4.63 if not excel_defaults else excel_defaults["costDiesel"], min_value=0.0)
    costDEF = st.number_input("DEF cost / gallon", value=6.0 if not excel_defaults else excel_defaults["costDEF"], min_value=0.0)

with colB:
    costOilFilter = st.number_input("Oil filter cost (per ODI)", value=0.0 if not excel_defaults else excel_defaults["costOilFilter"], min_value=0.0)
    laborRate = st.number_input("Fully-loaded labor $/hr", value=75.0 if not excel_defaults else excel_defaults["laborRate"], min_value=0.0)
    quartsPerODI = st.number_input("Quarts used per ODI", value=10 if not excel_defaults else int(excel_defaults["quartsPerODI"]), min_value=0)
    odiMiles = st.number_input("Current ODI miles", value=10000 if not excel_defaults else int(excel_defaults["odiMiles"]), step=100, min_value=1)
    odiMultiplierX = st.number_input("New ODI multiplier (X)", value=1.5 if not excel_defaults else excel_defaults["odiMultiplierX"], step=0.1, min_value=0.1)

with colC:
    laborHoursPerODI = st.number_input("Labor hours per ODI", value=1.0 if not excel_defaults else excel_defaults["laborHoursPerODI"], step=0.1, min_value=0.0)
    currentMPG = st.number_input("Current MPG", value=12.0 if not excel_defaults else excel_defaults["currentMPG"], step=0.1, min_value=0.1)
    mpgIncreasePct = st.number_input("Modeled % MPG increase", value=5.0 if not excel_defaults else excel_defaults["mpgIncreasePct"], step=0.1, min_value=0.0)
    defGalPer100Fuel = st.number_input("DEF gallons / 100 gallons fuel", value=3.0 if not excel_defaults else excel_defaults["defGalPer100Fuel"], step=0.1, min_value=0.0)
    defReductionPct = st.number_input("Modeled % DEF reduction", value=10.0 if not excel_defaults else excel_defaults["defReductionPct"], step=0.1, min_value=0.0)

st.markdown("---")
st.subheader("DPF Service")

col1, col2, col3, col4 = st.columns(4)
with col1:
    dpfIntervalMiles = st.number_input("Current DPF service interval (miles)", value=350000 if not excel_defaults else int(excel_defaults["dpfIntervalMiles"]), step=1000, min_value=1)
with col2:
    dpfMultiplierX = st.number_input("New DPF interval multiplier (X)", value=1.5 if not excel_defaults else excel_defaults["dpfMultiplierX"], step=0.1, min_value=0.1)
with col3:
    dpfLaborHours = st.number_input("DPF labor hours / service", value=2.0 if not excel_defaults else excel_defaults["dpfLaborHours"], step=0.1, min_value=0.0)
with col4:
    useReplace = st.checkbox("Use replacement (instead of refurbish)", value=False)

col5, col6 = st.columns(2)
with col5:
    dpfRefurbishCost = st.number_input("DPF refurbish cost (parts)", value=1500.0 if not excel_defaults else excel_defaults["dpfRefurbishCost"], min_value=0.0)
with col6:
    dpfReplaceCost = st.number_input("DPF replace cost (parts)", value=4000.0 if not excel_defaults else excel_defaults["dpfReplaceCost"], min_value=0.0)

# --- CALCULATIONS ---
mpgNew = currentMPG * (1 + mpgIncreasePct / 100.0)
fuelGalCurrent = miles / currentMPG
fuelGalNew = miles / mpgNew
fuelCostCurrent = fuelGalCurrent * costDiesel
fuelCostNew = fuelGalNew * costDiesel
fuelSavings = fuelCostCurrent - fuelCostNew

defGalCurrent = fuelGalCurrent * (defGalPer100Fuel / 100.0)
defGalNew = defGalCurrent * (1 - defReductionPct / 100.0)
defCostCurrent = defGalCurrent * costDEF
defCostNew = defGalNew * costDEF
defSavings = defCostCurrent - defCostNew

odiNewMiles = odiMiles * odiMultiplierX
nODICurrent = miles / odiMiles
nODINew = miles / odiNewMiles
oilPartsCurrent = nODICurrent * quartsPerODI * costQuartIncumbent + nODICurrent * costOilFilter
oilPartsNew = nODINew * quartsPerODI * costQuartEvolve + nODINew * costOilFilter
oilLaborCurrent = nODICurrent * laborHoursPerODI * laborRate
oilLaborNew = nODINew * laborHoursPerODI * laborRate
oilTotalCurrent = oilPartsCurrent + oilLaborCurrent
oilTotalNew = oilPartsNew + oilLaborNew
oilSavings = oilTotalCurrent - oilTotalNew

dpfNewInterval = dpfIntervalMiles * dpfMultiplierX
nDPFCurrent = miles / dpfIntervalMiles
nDPFNew = miles / dpfNewInterval
dpfUnitParts = dpfReplaceCost if useReplace else dpfRefurbishCost
dpfServiceCostCurrent = nDPFCurrent * (dpfUnitParts + dpfLaborHours * laborRate)
dpfServiceCostNew = nDPFNew * (dpfUnitParts + dpfLaborHours * laborRate)
dpfSavings = dpfServiceCostCurrent - dpfServiceCostNew

currentTotal = fuelCostCurrent + defCostCurrent + oilTotalCurrent + dpfServiceCostCurrent
newTotal = fuelCostNew + defCostNew + oilTotalNew + dpfServiceCostNew
totalSavings = currentTotal - newTotal
incrementalLubeSpend = max(0.0, oilPartsNew - nODICurrent * quartsPerODI * costQuartIncumbent)
roiPct = (totalSavings / incrementalLubeSpend * 100.0) if incrementalLubeSpend > 0 else float("inf")
savingsPerMile = totalSavings / miles if miles > 0 else 0.0
paybackMiles = (incrementalLubeSpend / savingsPerMile) if (incrementalLubeSpend > 0 and savingsPerMile > 0) else 0.0

# --- REPORT (HTML) ---
def dollars(x):
    if math.isinf(x):
        return "∞"
    return "${:,.2f}".format(x)

def build_report_html():
    rows = [
        ("New MPG (modeled)", f"{mpgNew:.2f} mpg"),
        ("Fuel savings", dollars(fuelSavings)),
        ("DEF savings", dollars(defSavings)),
        ("Oil & labor savings", dollars(oilSavings)),
        ("DPF savings", dollars(dpfSavings)),
        ("Total savings", dollars(totalSavings)),
        ("Incremental lube spend", dollars(incrementalLubeSpend)),
        ("ROI", "∞%" if math.isinf(roiPct) else f"{roiPct:.1f}%"),
        ("Payback miles (approx)", f"{paybackMiles:,.0f}" if paybackMiles > 0 else "—"),
        ("Savings per mile", dollars(savingsPerMile)),
    ]
    inputs_map = {
        "Miles traveled": miles,
        "Cost / qt — Evolve": costQuartEvolve,
        "Cost / qt — Incumbent": costQuartIncumbent,
        "Diesel $/gal": costDiesel,
        "DEF $/gal": costDEF,
        "Oil filter $/ODI": costOilFilter,
        "Labor $/hr": laborRate,
        "Quarts / ODI": quartsPerODI,
        "Current ODI miles": odiMiles,
        "ODI multiplier (X)": odiMultiplierX,
        "Labor hours / ODI": laborHoursPerODI,
        "Current MPG": currentMPG,
        "MPG increase %": mpgIncreasePct,
        "DEF gal /100 fuel": defGalPer100Fuel,
        "DEF reduction %": defReductionPct,
        "DPF interval (miles)": dpfIntervalMiles,
        "DPF multiplier (X)": dpfMultiplierX,
        "DPF labor hours": dpfLaborHours,
        "DPF refurbish $": dpfRefurbishCost,
        "DPF replace $": dpfReplaceCost,
        "Use replacement": "Yes" if useReplace else "No",
    }
    head = """
<!doctype html><html><head><meta charset='utf-8'/>
<title>Evolve ROI Report</title>
<style>
 body{font-family:-apple-system, Segoe UI, Roboto, Helvetica, Arial; margin:40px; color:#0b3d2e}
 h1,h2{color:#0b3d2e}
 .wrap{max-width:920px;margin:0 auto}
 .logo{height:48px;vertical-align:middle;margin-right:10px}
 table{border-collapse:collapse;width:100%;margin:12px 0}
 th,td{border:1px solid #cde6d6;padding:10px;text-align:left}
 th{background:#e6f4ea}
 .note{color:#256d4f;font-size:13px}
 @media print{ .noprint{display:none} }
</style>
</head><body><div class="wrap">
"""
    logo64 = "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"
    top = f"<h1><img class='logo' src='data:image/png;base64,{logo64}'/>Evolve® HDD Tractor ROI Report</h1>"
    key_rows = "".join([f"<tr><th>{k}</th><td>{v}</td></tr>" for k,v in rows])
    inp_rows = "".join([f"<tr><th>{k}</th><td>{v}</td></tr>" for k,v in inputs_map.items()])
    html = head + top + "<h2>Key Outputs</h2><table><tbody>" + key_rows + "</tbody></table>" + \
           "<h2>Inputs</h2><table><tbody>" + inp_rows + "</tbody></table>" + \
           "<p class='note noprint'>Tip: Print → Save as PDF.</p></div></body></html>"
    return html.encode("utf-8")

st.markdown("---")
st.subheader("Key Outputs")

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("New MPG (modeled)", f"{mpgNew:.2f}")
    st.metric("Fuel savings", dollars(fuelSavings))
with c2:
    st.metric("DEF savings", dollars(defSavings))
    st.metric("Oil & labor savings", dollars(oilSavings))
with c3:
    st.metric("DPF savings", dollars(dpfSavings))
    st.metric("Total savings", dollars(totalSavings))
with c4:
    st.metric("Incremental lube spend", dollars(incrementalLubeSpend))
    st.metric("ROI", "∞%" if math.isinf(roiPct) else f"{roiPct:.1f}%")

st.markdown("### Cost Breakdown (Current → New)")
cb1, cb2, cb3 = st.columns(3)
with cb1:
    st.write("**Fuel Cost**")
    st.write(f"{dollars(fuelCostCurrent)} → {dollars(fuelCostNew)}")
    st.write("**DEF Cost**")
    st.write(f"{dollars(defCostCurrent)} → {dollars(defCostNew)}")
with cb2:
    st.write("**Oil Parts**")
    st.write(f"{dollars(oilPartsCurrent)} → {dollars(oilPartsNew)}")
    st.write("**Oil Labor**")
    st.write(f"{dollars(oilLaborCurrent)} → {dollars(oilLaborNew)}")
with cb3:
    st.write("**DPF Service**")
    st.write(f"{dollars(dpfServiceCostCurrent)} → {dollars(dpfServiceCostNew)}")
    st.write("**Payback Miles (approx)**")
    st.write(f"{paybackMiles:,.0f}" if paybackMiles > 0 else "—")
    st.write("**Savings per Mile**")
    st.write(dollars(savingsPerMile))

report_bytes = build_report_html()
st.download_button("Download Formal Report (HTML / print to PDF)", data=report_bytes, file_name="evolve_roi_report.html", mime="text/html")

st.info("""
**Notes & Assumptions**  
• New MPG = Current MPG × (1 + MPG increase %).  
• DEF usage reduced by the modeled %.  
• New ODI miles = Current ODI miles × ODI multiplier. Labor scales by hours per ODI.  
• New DPF interval = Current interval × DPF multiplier. DPF service cost = parts (refurbish or replace) + labor × hours.  
• ROI uses incremental lubricant parts spend as the investment baseline; payback miles ≈ incremental spend ÷ savings per mile.
""")
