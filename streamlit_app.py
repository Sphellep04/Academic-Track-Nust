import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from scipy import stats
from io import BytesIO

# ── Page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Academic Dashboard | Shapopi Phellep",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Theme colours ──────────────────────────────────────────────────────────
PASS_COL  = "#4CAF50"
FAIL_COL  = "#F44336"
BLUE      = "#2196F3"
ORANGE    = "#FF9800"

# ── Raw data ───────────────────────────────────────────────────────────────
RAW = [
    (2021,"Year 1",1,"Sem 1","Introduction to Computing","ICG",61,"Pass"),
    (2021,"Year 1",1,"Sem 1","Design Thinking","DST",60,"Pass"),
    (2021,"Year 1",1,"Sem 1","Database Fundamentals","DBF",53,"Pass"),
    (2021,"Year 1",1,"Sem 1","Math for Computing 1","MCI",55,"Pass"),
    (2021,"Year 1",1,"Sem 1","Business Management Info Systems","BMC",57,"Pass"),
    (2021,"Year 1",2,"Sem 2","Database Programming","DGP",50,"Pass"),
    (2021,"Year 1",2,"Sem 2","Computer Organisation & Architecture","COA",56,"Pass"),
    (2021,"Year 1",2,"Sem 2","Data Structures & Algorithm 1","DSA1",50,"Pass"),
    (2021,"Year 1",2,"Sem 2","Math for Computing 2","MCI2",70,"Pass"),
    (2021,"Year 1",2,"Sem 2","Programming 1","PRG1",61,"Pass"),
    (2022,"Year 2",3,"Sem 3","Applied Statistics & Probability","ASP",36,"Fail"),
    (2022,"Year 2",3,"Sem 3","Data Networks","DTN",None,"Fail"),
    (2022,"Year 2",3,"Sem 3","Information System Security","ISS",57,"Pass"),
    (2022,"Year 2",3,"Sem 3","Operating Systems","OPS",50,"Pass"),
    (2022,"Year 2",3,"Sem 3","Programming 2","PRG2",30,"Fail"),
    (2022,"Year 2",3,"Sem 3","English for Academic Purposes","EAP",50,"Pass"),
    (2022,"Year 2",4,"Sem 4","Ethics for Computing","EFC",60,"Pass"),
    (2022,"Year 2",4,"Sem 4","Innovation Creativity & Entre","ICE",34,"Fail"),
    (2023,"Year 2",3,"Sem 3","Applied Statistics & Probability","ASP",58,"Pass"),
    (2023,"Year 2",3,"Sem 3","Data Networks","DTN",None,"Fail"),
    (2023,"Year 2",3,"Sem 3","Programming 2","PRG2",16,"Fail"),
    (2023,"Year 2",4,"Sem 4","Data Analytics","DTA",52,"Pass"),
    (2023,"Year 2",4,"Sem 4","Innovation Creativity & Entre","ICE",66,"Pass"),
    (2024,"Year 3",5,"Sem 5","Data Structures & Algorithm 2","DSA2",74,"Pass"),
    (2024,"Year 3",5,"Sem 5","Software Processes","SPS",53,"Pass"),
    (2024,"Year 3",5,"Sem 5","Software Verification & Validation","SVV",28,"Fail"),
    (2024,"Year 3",5,"Sem 5","Programming 2","PRG2",75,"Pass"),
    (2024,"Year 3",6,"Sem 6","Project Management for IT","PTM",66,"Pass"),
    (2024,"Year 3",6,"Sem 6","Sustainability & Development","SYD",68,"Pass"),
    (2024,"Year 3",6,"Sem 6","Web Development","WAD",63,"Pass"),
    (2024,"Year 3",6,"Sem 6","Distributed Systems & Applications","DSA",62,"Pass"),
    (2025,"Year 4",7,"Sem 7","Artificial Intelligence","ARI",65,"Pass"),
    (2025,"Year 4",7,"Sem 7","Compiler Techniques","CTE",73,"Pass"),
    (2025,"Year 4",7,"Sem 7","Mobile Application Development","MAP",53,"Pass"),
    (2025,"Year 4",7,"Sem 7","Data Networks","DTN",38,"Fail"),
    (2025,"Year 4",7,"Sem 7","Software Verification & Validation","SVV",60,"Pass"),
]

COLS = ["Year","Study_Year","Sem_Num","Sem_Label","Course","Code","Marks","Result"]

EXCEL_PATH = r"C:\Users\AdminTC\OneDrive - NUST\Documents\Academic Track\Academic track.xlsx"

SKILL_MAP = {
    "Programming & Dev":     ["PRG1", "PRG2", "DGP", "CTE", "MAP", "WAD"],
    "Data & Analytics":      ["DBF", "DTA", "ASP"],
    "Mathematics":           ["MCI", "MCI2"],
    "Systems & Networks":    ["COA", "OPS", "DTN", "DSA", "DSA1"],
    "Software Engineering":  ["SPS", "SVV", "PTM"],
    "Security & Ethics":     ["ISS", "EFC"],
    "Innovation & Business": ["BMC", "DST", "ICE", "SYD", "EAP", "ICG"],
    "AI & Algorithms":       ["ARI", "DSA2"],
}

def parse_excel(source):
    raw = pd.read_excel(source, header=5, usecols="A:G", engine="openpyxl")
    raw.columns = ["Year", "Study_Year", "Sem_Label", "Course", "Code", "Marks", "Result"]
    raw["Year"]       = pd.to_numeric(raw["Year"], errors="coerce").ffill()
    raw["Study_Year"] = raw["Study_Year"].ffill()
    raw["Sem_Label"]  = raw["Sem_Label"].ffill()
    # Drop rows with no course code (separators / empty rows)
    raw = raw[raw["Code"].notna() & (~raw["Code"].astype(str).str.strip().isin(["", "Course Code"]))]
    # Keep only Pass/Fail rows
    raw["Result"] = raw["Result"].astype(str).str.strip()
    raw = raw[raw["Result"].isin(["Pass", "Fail"])]
    raw["Marks"]      = pd.to_numeric(raw["Marks"].replace({"N/A": None}), errors="coerce")
    raw["Sem_Label"]  = raw["Sem_Label"].astype(str).str.replace("Semester ", "Sem ", regex=False)
    raw["Sem_Num"]    = raw["Sem_Label"].str.extract(r"(\d+)").astype(float).fillna(0).astype(int)
    raw["Year"]       = raw["Year"].fillna(0).astype(int)
    raw["Course"]     = raw["Course"].astype(str).str.strip()
    raw["Code"]       = raw["Code"].astype(str).str.strip()
    return raw[COLS].reset_index(drop=True)

def enrich(df):
    df["Passed"]     = df["Result"] == "Pass"
    df["Grade"]      = df["Marks"].apply(grade_letter)
    df["GPA_Points"] = df["Marks"].apply(marks_to_gpa)
    return df

@st.cache_data
def load_from_records():
    return enrich(pd.DataFrame(RAW, columns=COLS))

def load_from_excel(source):
    return enrich(parse_excel(source))

def grade_letter(m):
    if pd.isna(m): return "N/A"
    if m >= 75: return "A"
    if m >= 65: return "B"
    if m >= 55: return "C"
    if m >= 50: return "D"
    return "F"

def marks_to_gpa(m):
    if pd.isna(m): return None
    if m >= 75: return 4.0
    if m >= 65: return 3.0
    if m >= 55: return 2.0
    if m >= 50: return 1.0
    return 0.0

def generate_pdf(df):
    from fpdf import FPDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Academic Report — Shapopi Phellep", ln=True, align="C")
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 8, "NUST | BSc Computer Science (Software Development)", ln=True, align="C")
    pdf.ln(6)

    graded = df[df["Marks"].notna()]
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Summary Statistics", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 6, f"Total modules attempted: {len(df)}", ln=True)
    pdf.cell(0, 6, f"Modules graded: {len(graded)}", ln=True)
    pdf.cell(0, 6, f"Pass rate: {100*graded['Passed'].mean():.1f}%", ln=True)
    pdf.cell(0, 6, f"Average mark: {graded['Marks'].mean():.1f}%", ln=True)
    pdf.cell(0, 6, f"GPA (est.): {graded['GPA_Points'].mean():.2f} / 4.00", ln=True)
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Module Record", ln=True)
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(10, 6, "Year", border=1)
    pdf.cell(20, 6, "Cal.Yr", border=1)
    pdf.cell(80, 6, "Course", border=1)
    pdf.cell(18, 6, "Code", border=1)
    pdf.cell(18, 6, "Marks", border=1)
    pdf.cell(20, 6, "Result", border=1, ln=True)
    pdf.set_font("Helvetica", "", 8)
    for _, row in df.iterrows():
        pdf.cell(10, 5, str(row["Study_Year"])[-1], border=1)
        pdf.cell(20, 5, str(row["Year"]), border=1)
        pdf.cell(80, 5, str(row["Course"])[:45], border=1)
        pdf.cell(18, 5, str(row["Code"]), border=1)
        pdf.cell(18, 5, str(row["Marks"]) if pd.notna(row["Marks"]) else "N/A", border=1)
        pdf.cell(20, 5, str(row["Result"]), border=1, ln=True)

    return bytes(pdf.output())

# ── Sidebar ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/en/thumb/3/35/NUST_Namibia_Logo.png/200px-NUST_Namibia_Logo.png",
             width=120, use_container_width=False)
    st.markdown("### Shapopi Phellep")
    st.caption("BSc CS — Software Development")
    st.divider()

    st.markdown("**Data Source**")
    uploaded = st.file_uploader("Upload Excel to update data", type=["xlsx"],
                                help="Upload your Academic track.xlsx to refresh all charts live.")
    st.divider()

    st.markdown("**Filters**")
    years = st.multiselect("Study Year", options=["Year 1","Year 2","Year 3","Year 4"],
                           default=["Year 1","Year 2","Year 3","Year 4"])
    result_filter = st.radio("Result", ["All", "Pass only", "Fail only"], horizontal=True)
    st.divider()
    st.caption("Built with Streamlit + Plotly")

# ── Load ───────────────────────────────────────────────────────────────────
import os

if uploaded is not None:
    try:
        df_all = load_from_excel(uploaded)
        st.sidebar.success("Live data loaded from Excel.")
    except Exception as e:
        st.sidebar.error(f"Could not read Excel: {e}")
        df_all = load_from_records()
elif os.path.exists(EXCEL_PATH):
    try:
        df_all = load_from_excel(EXCEL_PATH)
        st.sidebar.info("Auto-loaded from local Excel file.")
    except Exception:
        df_all = load_from_records()
else:
    df_all = load_from_records()

df_graded = df_all[df_all["Marks"].notna()].copy()

# Apply filters
df_view = df_graded[df_graded["Study_Year"].isin(years)].copy()
if result_filter == "Pass only":
    df_view = df_view[df_view["Passed"]]
elif result_filter == "Fail only":
    df_view = df_view[~df_view["Passed"]]

# ── Tabs ───────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "📊 Overview", "📈 Charts", "📋 Module Details",
    "🔁 Retake Tracker", "🧮 GPA Calculator", "🎯 What-If Simulator",
    "📖 My Story", "🕸️ Skills Radar"
])

# ══════════════════════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ══════════════════════════════════════════════════════════════════════════
with tab1:
    st.title("🎓 Academic Dashboard")
    st.markdown("**Namibia University of Science and Technology** — Academic Progress Report")
    st.divider()

    # KPI cards
    total        = len(df_all)
    n_graded     = len(df_graded)
    n_pass       = int(df_graded["Passed"].sum())
    n_fail       = int((~df_graded["Passed"]).sum())
    avg_mark     = df_graded["Marks"].mean()
    gpa          = df_graded["GPA_Points"].mean()
    pass_rate    = 100 * n_pass / n_graded

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Modules Attempted", total)
    c2.metric("Pass Rate", f"{pass_rate:.1f}%", f"{n_pass} passed")
    c3.metric("Average Mark", f"{avg_mark:.1f}%")
    c4.metric("Est. GPA", f"{gpa:.2f} / 4.00")
    c5.metric("Outstanding Fails", n_fail, delta_color="inverse")

    st.divider()
    col_l, col_r = st.columns(2)

    # Year-by-year summary table
    with col_l:
        st.markdown("#### Progress by Study Year")
        year_summary = df_graded.groupby("Study_Year").agg(
            Modules=("Marks","count"),
            Avg_Mark=("Marks","mean"),
            Pass_Rate=("Passed", lambda x: f"{100*x.mean():.0f}%"),
            GPA=("GPA_Points","mean"),
        ).reset_index().rename(columns={"Study_Year":"Year","Avg_Mark":"Avg Mark (%)","Pass_Rate":"Pass Rate"})
        year_summary["Avg Mark (%)"] = year_summary["Avg Mark (%)"].round(1)
        year_summary["GPA"] = year_summary["GPA"].round(2)
        st.dataframe(year_summary.set_index("Year"), use_container_width=True)

    # Grade distribution donut
    with col_r:
        st.markdown("#### Grade Distribution")
        grade_order = ["A","B","C","D","F"]
        grade_colors = ["#1B5E20","#388E3C","#F9A825","#FB8C00","#C62828"]
        grade_counts = df_graded["Grade"].value_counts().reindex(grade_order, fill_value=0)
        fig_donut = go.Figure(go.Pie(
            labels=grade_counts.index,
            values=grade_counts.values,
            hole=0.5,
            marker_colors=grade_colors,
            textinfo="label+percent+value",
        ))
        fig_donut.update_layout(height=300, margin=dict(t=10,b=10,l=10,r=10),
                                showlegend=False)
        st.plotly_chart(fig_donut, use_container_width=True)

    st.divider()

    # Timeline summary
    st.markdown("#### Academic Timeline")
    timeline_data = [
        {"Year": "2021", "Event": "Enrolled at NUST — Year 1 begins", "Status": "✅"},
        {"Year": "2022", "Event": "Year 2 Sem 3 — First fails (ASP, PRG2, ICE, DTN)", "Status": "⚠️"},
        {"Year": "2023", "Event": "Retook Sem 3 & 4 — Cleared ASP & ICE, PRG2 still failing", "Status": "🔁"},
        {"Year": "2024", "Event": "Year 3 — Cleared PRG2 (75%). SVV failed, then passed in 2025", "Status": "📈"},
        {"Year": "2025", "Event": "Year 4 — 4 passes, DTN still outstanding", "Status": "🎯"},
    ]
    st.dataframe(pd.DataFrame(timeline_data).set_index("Year"), use_container_width=True)

    # PDF download
    st.divider()
    st.markdown("#### Export Report")
    if st.button("📄 Generate PDF Report"):
        pdf_bytes = generate_pdf(df_all)
        st.download_button("⬇️ Download PDF", data=pdf_bytes,
                           file_name="Shapopi_Academic_Report.pdf", mime="application/pdf")

# ══════════════════════════════════════════════════════════════════════════
# TAB 2 — CHARTS
# ══════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("### Interactive Charts")
    st.caption("Hover over any chart for details. Use filters in the sidebar to drill down.")

    # Chart 1: All module marks
    st.markdown("#### All Module Marks")
    fig1 = px.bar(
        df_view,
        x="Code", y="Marks", color="Result",
        color_discrete_map={"Pass": PASS_COL, "Fail": FAIL_COL},
        hover_data=["Course","Year","Study_Year","Sem_Label"],
        text="Marks",
        title="Final Marks per Module (filtered)",
    )
    fig1.add_hline(y=50, line_dash="dash", line_color="gray", annotation_text="Pass mark (50%)")
    fig1.add_hline(y=df_view["Marks"].mean(), line_dash="dot", line_color=BLUE,
                   annotation_text=f"Avg ({df_view['Marks'].mean():.1f}%)")
    fig1.update_traces(textposition="outside")
    fig1.update_layout(height=420, xaxis_title="Module Code", yaxis_title="Mark (%)",
                       yaxis_range=[0,105], legend_title="Result")
    st.plotly_chart(fig1, use_container_width=True)

    col1, col2 = st.columns(2)

    # Chart 2: Avg by study year + pass rate
    with col1:
        st.markdown("#### Avg Mark & Pass Rate by Year")
        yr_stats = df_graded.groupby("Study_Year").agg(
            avg=("Marks","mean"), pass_rate=("Passed", lambda x: 100*x.mean())
        ).reset_index()
        fig2 = make_subplots(specs=[[{"secondary_y": True}]])
        fig2.add_trace(go.Bar(x=yr_stats["Study_Year"], y=yr_stats["avg"],
                              name="Avg Mark", marker_color=BLUE, opacity=0.8), secondary_y=False)
        fig2.add_trace(go.Scatter(x=yr_stats["Study_Year"], y=yr_stats["pass_rate"],
                                  name="Pass Rate", mode="lines+markers",
                                  marker=dict(size=10), line=dict(color="#E91E63", width=2.5)),
                       secondary_y=True)
        fig2.add_hline(y=50, line_dash="dash", line_color="gray", secondary_y=False)
        fig2.update_yaxes(title_text="Average Mark (%)", secondary_y=False, range=[0,100])
        fig2.update_yaxes(title_text="Pass Rate (%)", secondary_y=True, range=[0,115])
        fig2.update_layout(height=380, legend=dict(orientation="h", y=1.12))
        st.plotly_chart(fig2, use_container_width=True)

    # Chart 3: Performance trend
    with col2:
        st.markdown("#### Performance Trend (2021–2025)")
        yr_trend = df_graded.groupby("Year")["Marks"].mean().reset_index()
        slope, intercept, r, _, _ = stats.linregress(yr_trend["Year"], yr_trend["Marks"])
        trend_y = slope * yr_trend["Year"] + intercept
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=yr_trend["Year"], y=yr_trend["Marks"],
                                  mode="lines+markers+text", name="Annual Avg",
                                  text=yr_trend["Marks"].round(1).astype(str) + "%",
                                  textposition="top center",
                                  marker=dict(size=10, color=BLUE),
                                  line=dict(width=2.5)))
        fig3.add_trace(go.Scatter(x=yr_trend["Year"], y=trend_y,
                                  mode="lines", name=f"Trend (slope={slope:+.1f}/yr)",
                                  line=dict(dash="dash", color=ORANGE, width=2)))
        fig3.add_hline(y=50, line_dash="dot", line_color="gray")
        fig3.update_layout(height=380, xaxis_title="Year", yaxis_title="Avg Mark (%)",
                           yaxis_range=[30,90])
        st.plotly_chart(fig3, use_container_width=True)

    # Chart 4: Box plot per year
    st.markdown("#### Score Distribution by Study Year")
    fig4 = px.box(df_graded, x="Study_Year", y="Marks", color="Study_Year",
                  points="all", hover_data=["Course","Code","Result"],
                  color_discrete_sequence=px.colors.qualitative.Set2)
    fig4.add_hline(y=50, line_dash="dash", line_color="gray", annotation_text="Pass mark")
    fig4.update_layout(height=400, showlegend=False,
                       xaxis_title="Study Year", yaxis_title="Mark (%)")
    st.plotly_chart(fig4, use_container_width=True)

    # Chart 5: Heatmap
    st.markdown("#### Module Marks Heatmap (Best/Final Attempt)")
    final_df = df_graded.sort_values("Year").drop_duplicates(subset=["Code"], keep="last")
    pivot = final_df.pivot_table(index="Study_Year", columns="Code", values="Marks", aggfunc="first")
    pivot = pivot.reindex(["Year 1","Year 2","Year 3","Year 4"])
    fig5 = px.imshow(pivot, text_auto=True, color_continuous_scale="RdYlGn",
                     zmin=0, zmax=100, aspect="auto",
                     labels=dict(color="Mark (%)"))
    fig5.update_layout(height=320, xaxis_title="Module Code", yaxis_title="Study Year")
    st.plotly_chart(fig5, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════
# TAB 3 — MODULE DETAILS
# ══════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("### Module Record")

    search = st.text_input("Search course name or code", placeholder="e.g. Programming, PRG2...")
    display_df = df_all.copy()
    if search:
        mask = (display_df["Course"].str.contains(search, case=False) |
                display_df["Code"].str.contains(search, case=False))
        display_df = display_df[mask]

    display_df["Marks"] = display_df["Marks"].apply(lambda x: f"{x:.0f}%" if pd.notna(x) else "N/A")
    styled = display_df[["Year","Study_Year","Sem_Label","Course","Code","Marks","Grade","Result"]].rename(
        columns={"Study_Year":"Study Year","Sem_Label":"Semester","Marks":"Final Mark"}
    )

    def colour_result(val):
        if val == "Pass": return "color: #2e7d32; font-weight: bold"
        if val == "Fail": return "color: #c62828; font-weight: bold"
        return ""

    st.dataframe(
        styled.style.map(colour_result, subset=["Result"]),
        use_container_width=True, height=500
    )
    st.caption(f"Showing {len(display_df)} of {len(df_all)} records")

# ══════════════════════════════════════════════════════════════════════════
# TAB 4 — RETAKE TRACKER
# ══════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("### Retake Tracker")
    st.caption("Modules attempted more than once, showing attempt-by-attempt progress.")

    retake_codes = df_all.groupby("Code").filter(lambda g: len(g) > 1)["Code"].unique()
    retake_df = df_all[df_all["Code"].isin(retake_codes)].sort_values(["Code","Year"])

    for code in retake_codes:
        sub = retake_df[retake_df["Code"] == code].reset_index(drop=True)
        course_name = sub.iloc[0]["Course"]
        final_status = sub.iloc[-1]["Result"]
        icon = "✅" if final_status == "Pass" else "❌"
        with st.expander(f"{icon} **{code}** — {course_name}  ({len(sub)} attempts)"):
            cols = st.columns(len(sub))
            for i, (col, (_, row)) in enumerate(zip(cols, sub.iterrows())):
                with col:
                    mark_str = f"{row['Marks']:.0f}%" if pd.notna(row["Marks"]) else "N/A"
                    color = PASS_COL if row["Result"] == "Pass" else FAIL_COL
                    st.markdown(
                        f"<div style='text-align:center; padding:12px; border-radius:8px;"
                        f"background:{color}22; border:1px solid {color}'>"
                        f"<b>Attempt {i+1}</b><br>{row['Year']}<br>"
                        f"<span style='font-size:1.4em;font-weight:bold'>{mark_str}</span><br>"
                        f"<span style='color:{color}'>{row['Result']}</span></div>",
                        unsafe_allow_html=True
                    )
            if sub["Marks"].notna().sum() > 1:
                marks_seq = sub[sub["Marks"].notna()][["Year","Marks","Result"]].copy()
                fig_rt = px.line(marks_seq, x="Year", y="Marks",
                                 markers=True, color_discrete_sequence=[BLUE])
                fig_rt.add_hline(y=50, line_dash="dash", line_color="gray")
                fig_rt.update_layout(height=200, margin=dict(t=10,b=10,l=10,r=10),
                                     yaxis_range=[0,100], yaxis_title="Mark (%)")
                st.plotly_chart(fig_rt, use_container_width=True)

    # Outstanding summary
    st.divider()
    outstanding = retake_df[retake_df["Result"] == "Fail"].groupby("Code").last().reset_index()
    outstanding = outstanding[outstanding["Code"].isin(
        retake_df.groupby("Code").filter(lambda g: g.iloc[-1]["Result"] == "Fail")["Code"].unique()
    )]
    if not outstanding.empty:
        st.markdown("#### Still Outstanding (Last Attempt = Fail)")
        st.dataframe(outstanding[["Code","Course","Year","Marks","Result"]].set_index("Code"),
                     use_container_width=True)
    else:
        st.success("All retaken modules have been cleared!")

# ══════════════════════════════════════════════════════════════════════════
# TAB 5 — GPA CALCULATOR
# ══════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown("### GPA Calculator")
    st.caption("Estimated GPA using a 4-point scale: A(≥75)=4.0 · B(≥65)=3.0 · C(≥55)=2.0 · D(≥50)=1.0 · F(<50)=0.0")

    final_for_gpa = df_graded.sort_values("Year").drop_duplicates(subset=["Code"], keep="last")
    gpa_overall   = final_for_gpa["GPA_Points"].mean()

    c1, c2, c3 = st.columns(3)
    c1.metric("Overall GPA (est.)", f"{gpa_overall:.2f} / 4.00")
    c2.metric("Classification",
              "First Class" if gpa_overall >= 3.5 else
              "Upper Second" if gpa_overall >= 3.0 else
              "Lower Second" if gpa_overall >= 2.5 else
              "Third Class" if gpa_overall >= 2.0 else "Pass")
    c3.metric("Modules used", len(final_for_gpa))

    st.divider()
    st.markdown("#### GPA by Study Year")
    yr_gpa = final_for_gpa.groupby("Study_Year")["GPA_Points"].mean().reset_index()
    fig_gpa = px.bar(yr_gpa, x="Study_Year", y="GPA_Points",
                     color="GPA_Points", color_continuous_scale="RdYlGn",
                     range_color=[0,4], text=yr_gpa["GPA_Points"].round(2),
                     labels={"GPA_Points":"GPA","Study_Year":"Study Year"})
    fig_gpa.update_traces(textposition="outside")
    fig_gpa.add_hline(y=gpa_overall, line_dash="dot", line_color=BLUE,
                      annotation_text=f"Overall avg: {gpa_overall:.2f}")
    fig_gpa.update_layout(height=350, yaxis_range=[0,4.5], coloraxis_showscale=False)
    st.plotly_chart(fig_gpa, use_container_width=True)

    st.divider()
    st.markdown("#### Module-Level GPA Breakdown")
    gpa_table = final_for_gpa[["Study_Year","Course","Code","Marks","Grade","GPA_Points"]].copy()
    gpa_table = gpa_table.sort_values(["Study_Year","GPA_Points"], ascending=[True,False])
    gpa_table["Marks"] = gpa_table["Marks"].apply(lambda x: f"{x:.0f}%")
    st.dataframe(gpa_table.rename(columns={"Study_Year":"Year","GPA_Points":"GPA Points"})
                 .set_index("Year"), use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════
# TAB 6 — WHAT-IF SIMULATOR
# ══════════════════════════════════════════════════════════════════════════
with tab6:
    st.markdown("### What-If Simulator")
    st.caption("Simulate how upcoming or pending results will affect your GPA and pass rate.")

    final_for_sim = df_graded.sort_values("Year").drop_duplicates(subset=["Code"], keep="last").copy()

    st.markdown("#### Pending / Upcoming Modules")
    st.markdown("Add modules you still need to complete and set expected marks:")

    pending_defaults = [
        {"Module": "Data Networks (DTN)", "Expected Mark": 55},
        {"Module": "New Module 1", "Expected Mark": 60},
    ]
    pending_df = pd.DataFrame(pending_defaults)
    edited = st.data_editor(
        pending_df, num_rows="dynamic", use_container_width=True,
        column_config={
            "Expected Mark": st.column_config.SliderColumn(min_value=0, max_value=100, step=1)
        }
    )

    if not edited.empty and edited["Expected Mark"].notna().any():
        sim_marks = edited["Expected Mark"].dropna().tolist()
        sim_gpa_points = [marks_to_gpa(m) for m in sim_marks]
        sim_passed = [m >= 50 for m in sim_marks]

        all_marks = list(final_for_sim["Marks"]) + sim_marks
        all_gpa   = list(final_for_sim["GPA_Points"]) + sim_gpa_points
        all_pass  = list(final_for_sim["Passed"])  + sim_passed

        new_avg      = np.mean(all_marks)
        new_gpa      = np.mean(all_gpa)
        new_pass_rate= 100 * np.mean(all_pass)

        st.divider()
        st.markdown("#### Projected Outcome")
        c1, c2, c3 = st.columns(3)
        c1.metric("Projected Avg Mark", f"{new_avg:.1f}%",
                  delta=f"{new_avg - df_graded['Marks'].mean():.1f}%")
        c2.metric("Projected GPA", f"{new_gpa:.2f}",
                  delta=f"{new_gpa - df_graded['GPA_Points'].mean():.2f}")
        c3.metric("Projected Pass Rate", f"{new_pass_rate:.1f}%",
                  delta=f"{new_pass_rate - 100*df_graded['Passed'].mean():.1f}%")

        st.markdown("#### Mark Needed to Hit a Target GPA")
        target_gpa = st.slider("Target GPA", 1.0, 4.0, 3.0, 0.1)
        n_current = len(final_for_sim)
        n_sim     = len(edited)
        needed_gpa_pts = (target_gpa * (n_current + n_sim) - final_for_sim["GPA_Points"].sum()) / max(n_sim,1)
        needed_mark = (
            75 if needed_gpa_pts >= 4.0 else
            65 if needed_gpa_pts >= 3.0 else
            55 if needed_gpa_pts >= 2.0 else
            50 if needed_gpa_pts >= 1.0 else 0
        )
        if needed_gpa_pts > 4.0:
            st.warning(f"A GPA of {target_gpa:.1f} is not achievable with {n_sim} pending module(s). Reduce target or add more modules.")
        else:
            st.info(f"To reach a GPA of **{target_gpa:.1f}**, you need roughly **{needed_mark}%+ (grade {grade_letter(needed_mark)})** on average across your {n_sim} pending module(s).")

# ══════════════════════════════════════════════════════════════════════════
# TAB 7 — MY STORY
# ══════════════════════════════════════════════════════════════════════════
with tab7:
    # Computed stats to embed in the story
    avg_y2 = df_graded[df_graded["Study_Year"] == "Year 2"]["Marks"].mean()
    avg_y3 = df_graded[df_graded["Study_Year"] == "Year 3"]["Marks"].mean()
    improvement = avg_y3 - avg_y2

    col_story, col_stats = st.columns([2, 1])

    with col_story:
        st.markdown("""
# The Story Behind the Numbers

> *People look at a transcript and see numbers. A grade here, a fail there, a retake somewhere in between.
> What they don't see is everything that sat behind those numbers — the commute you couldn't afford,
> the laptop that could barely open two tabs, the test you missed because the month had run out before it had.*

---

### Before NUST

I didn't start here. Before NUST, I was at UNAM studying Secondary Education — Mathematics and Physical
Science. On paper, a solid path. In reality, it wasn't mine.

I was a dancer. Still am, in some way that never fully leaves you. But dancing came with a circle, and
that circle wasn't pointed anywhere good. I knew it, and I knew I had to make a move — not just change
institutions, but change environments entirely. So I made a decision: go to Windhoek, stop dancing,
reset, and rebuild.

What I didn't know was that **Windhoek has its own jungle.**

---

### Year 1 Was Fine — Until It Wasn't

First year at NUST went reasonably well. New city, new degree, new version of myself — I was motivated.
But the city has a pull of its own, and somewhere between orientation and second semester, I got carried
away. Not dramatically. Just slowly, the way focus slips when you're not watching it.

Then Year 2 came, and the weight of everything started to show up in the numbers.

Living in Katutura — one of the furthest points from campus — meant that getting to a lecture wasn't
just a matter of showing up. It was a budget decision. Some mornings, the money wasn't there, so
neither was I. Missed classes turned into missed tests. Late submissions. Pressure stacking up with
nowhere to put it.

The laptop situation didn't help. A Lenovo with 2GB of RAM is a documentation machine at best. I couldn't
practice, couldn't run environments, couldn't do half the practical work the degree required. I learned
what I could, when I could, with what I had. Looking back, investing in a proper machine earlier would
have changed a lot — but I wasn't wise enough then to see it as an investment rather than an expense.

Trading also found its way into the picture at some point — another pull on attention, time, and focus.
I won't draw it all out, but it had its effect. What I will say is that I've since found a way to carry
all of it — trading, work, school, and life — without any one of them swallowing the others. That balance
took real time to build. But it's built.

Those were hard years. The data shows it clearly — 2022 was my lowest point, three fails in one semester.
That's not a statistic I'm hiding. It's a chapter I earned.

---

### Making the Move

In 2023, I made a plan and moved closer to campus. It sounds small. It wasn't.

Proximity changed everything. Getting to class was no longer a financial calculation. I was present more,
engaged more, and the results followed almost immediately. **The grades climbed.** You can see it in the
charts — the upward trend from 2023 onward isn't luck. It's what consistency looks like when the basic
barriers are finally removed.

That move was one of the best decisions I made in this degree.

---

### DTN and the Long Game

If one module has defined the difficulty of this journey, it's **DTN — Data Networks.** Three attempts,
various circumstances. It has been the stubborn one.

But something shifted when formal academics paused and the real world began.

In the second semester of 2025, I had no modules and no internship secured. Instead of waiting it out,
I entered the **MICT Hackathon** — partly out of determination, partly because it was the only door I
could see. We made it through. That hackathon led directly to an internship opportunity at **Salt Essentials IT**,
and on **2 February 2026** I walked in for my first day of work. That opportunity turned into an education
of a completely different kind.

At Salt, I was doing real work for the first time. Internal projects, industry exposure, and labs —
networking labs, specifically — that started to unlock things DTN had been trying to teach me in theory.
Practical experience did what textbooks couldn't quite do alone.

I'm currently doing my **WIL (Work Integrated Learning).** My first DTN test came back at **66%.**
For that module, and where I've come from with it, that number means more to me than any A I've received.
DTN is the last wall, and it's coming down.

---

### Where I Am Now

**Expected graduation: October 2026.**

The dashboard you're looking at is a record of four years of navigating a degree with limited resources,
the wrong environments, costly mistakes, and — eventually — the kind of growth that only comes from being
genuinely tested.

I started this as a student who had too much going on and not enough going right.
I'm finishing it as someone who learned, slowly and sometimes painfully, what it takes to stay the course.

**The grades got better. So did I.**

---
*BSc Computer Science — Software Development | Namibia University of Science and Technology*
""")

    with col_stats:
        st.markdown("### By the Numbers")
        st.markdown("<br>", unsafe_allow_html=True)

        # Callout cards
        def stat_card(label, value, note="", color="#2196F3"):
            st.markdown(
                f"""<div style='padding:16px;border-radius:10px;background:{color}18;
                border-left:4px solid {color};margin-bottom:12px'>
                <div style='font-size:0.8em;color:#888'>{label}</div>
                <div style='font-size:1.6em;font-weight:700;color:{color}'>{value}</div>
                <div style='font-size:0.75em;color:#666'>{note}</div></div>""",
                unsafe_allow_html=True
            )

        stat_card("Years at NUST", "4", "2021 – 2025", BLUE)
        stat_card("Modules Attempted", str(len(df_all)), "across all semesters", BLUE)
        stat_card("Overall Pass Rate", f"{100*df_graded['Passed'].mean():.0f}%",
                  f"{int(df_graded['Passed'].sum())} passed", PASS_COL)
        stat_card(
            "Grade Improvement",
            f"+{improvement:.1f}%",
            "Year 2 → Year 3 average",
            "#FF9800"
        )
        stat_card("DTN Test (2026)", "66%", "First test at Salt — best yet", "#9C27B0")
        stat_card("Graduation Target", "Oct 2026", "WIL in progress", PASS_COL)

        st.divider()
        st.markdown("##### Journey in One Line")
        st.info(
            "From 2GB RAM to destiny — "
            "the machine had limits. I never did."
        )

# ══════════════════════════════════════════════════════════════════════════
# TAB 8 — SKILLS RADAR
# ══════════════════════════════════════════════════════════════════════════
with tab8:
    st.markdown("### Skills Radar")
    st.caption(
        "Each domain is scored by the average final mark across its modules. "
        "Shows where your strengths are and where growth happened."
    )

    # Use best/final attempt per module for the radar
    final_radar = df_graded.sort_values("Year").drop_duplicates(subset=["Code"], keep="last")

    # Build domain scores
    domain_scores, domain_modules, domain_details = [], [], []
    for domain, codes in SKILL_MAP.items():
        subset = final_radar[final_radar["Code"].isin(codes)]
        if not subset.empty:
            avg  = subset["Marks"].mean()
            mods = ", ".join(
                f"{r['Code']} ({r['Marks']:.0f}%)" for _, r in subset.iterrows()
            )
            detail = subset[["Course","Code","Marks","Result"]].copy()
        else:
            avg  = 0
            mods = "No data"
            detail = pd.DataFrame()
        domain_scores.append(round(avg, 1))
        domain_modules.append(mods)
        domain_details.append(detail)

    domains = list(SKILL_MAP.keys())

    col_radar, col_breakdown = st.columns([1, 1])

    with col_radar:
        # Close the polygon by repeating the first value
        r_vals   = domain_scores + [domain_scores[0]]
        theta    = domains + [domains[0]]
        hover    = domain_modules + [domain_modules[0]]

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=r_vals,
            theta=theta,
            fill="toself",
            fillcolor="rgba(33, 150, 243, 0.15)",
            line=dict(color=BLUE, width=2.5),
            marker=dict(size=7, color=BLUE),
            text=hover,
            hovertemplate="<b>%{theta}</b><br>Avg: %{r}%<br>%{text}<extra></extra>",
            name="Skill Score",
        ))
        # 50% reference ring
        fig_radar.add_trace(go.Scatterpolar(
            r=[50] * (len(domains) + 1),
            theta=theta,
            mode="lines",
            line=dict(color="gray", dash="dash", width=1),
            showlegend=False,
            hoverinfo="skip",
        ))
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100],
                                tickvals=[25, 50, 75, 100],
                                tickfont=dict(size=9)),
                angularaxis=dict(tickfont=dict(size=11)),
            ),
            showlegend=False,
            height=500,
            margin=dict(t=30, b=30, l=60, r=60),
        )
        st.plotly_chart(fig_radar, use_container_width=True)

        # Strongest / weakest callout
        scored = [(d, s) for d, s in zip(domains, domain_scores) if s > 0]
        if scored:
            best_d,  best_s  = max(scored, key=lambda x: x[1])
            worst_d, worst_s = min(scored, key=lambda x: x[1])
            c1, c2 = st.columns(2)
            c1.metric("Strongest Domain", best_d,  f"{best_s:.1f}%")
            c2.metric("Growth Opportunity", worst_d, f"{worst_s:.1f}%")

    with col_breakdown:
        st.markdown("#### Domain Breakdown")
        for domain, score, mods_str, detail in zip(domains, domain_scores, domain_modules, domain_details):
            color = (PASS_COL if score >= 65 else
                     ORANGE   if score >= 50 else
                     FAIL_COL if score > 0  else "#9E9E9E")
            with st.expander(f"**{domain}** — {score:.1f}%"):
                if not detail.empty:
                    detail_show = detail.copy()
                    detail_show["Marks"] = detail_show["Marks"].apply(lambda x: f"{x:.0f}%")
                    st.dataframe(
                        detail_show.rename(columns={"Marks":"Final Mark"})
                                   .set_index("Code"),
                        use_container_width=True
                    )
                    # Mini bar for this domain
                    fig_mini = px.bar(
                        detail, x="Code", y="Marks",
                        color="Result",
                        color_discrete_map={"Pass": PASS_COL, "Fail": FAIL_COL},
                        text="Marks",
                    )
                    fig_mini.add_hline(y=50, line_dash="dash", line_color="gray")
                    fig_mini.update_traces(texttemplate="%{text:.0f}%", textposition="outside")
                    fig_mini.update_layout(
                        height=200, showlegend=False,
                        margin=dict(t=5, b=5, l=5, r=5),
                        yaxis_range=[0, 105],
                        xaxis_title="", yaxis_title="Mark (%)",
                    )
                    st.plotly_chart(fig_mini, use_container_width=True)
                else:
                    st.caption("No graded modules mapped to this domain yet.")

    st.divider()
    st.markdown("#### All Domains at a Glance")
    radar_df = pd.DataFrame({
        "Domain": domains,
        "Avg Mark (%)": domain_scores,
        "Modules": domain_modules,
    }).sort_values("Avg Mark (%)", ascending=False)
    radar_df["Avg Mark (%)"] = radar_df["Avg Mark (%)"].apply(
        lambda x: f"{x:.1f}%" if x > 0 else "No data"
    )
    st.dataframe(radar_df.set_index("Domain"), use_container_width=True)
