import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- Sidebar navigation ----------
with st.sidebar:
    st.markdown("## 🏦 Loan Approval System")
    st.caption("Application navigation")
    st.page_link("Home.py", label="Home", icon="🏠")
    st.page_link("pages/Analysis.py", label="Analysis", icon="📊")
    st.page_link("pages/Prediction.py", label="Prediction", icon="📝")
    st.divider()

# ---------- لوحة ألوان حيوية (Vivid) بدل الألوان الهادية اللي كانت قبل كده ----------
NAVY = "#14304D"
TEXT_SECONDARY = "#6B7280"
CARD_BG = "#F7F8FA"
CARD_BORDER = "#E3E6EB"
BLUE = "#3B82F6"
RED = "#EF4444"
GREEN = "#22C55E"
AMBER = "#F59E0B"
PURPLE = "#8B5CF6"
CYAN = "#06B6D4"
PINK = "#EC4899"

# لستة ألوان بنلف عليها في أي رسمة فيها أكتر من فئة (Employment Type, Loan Purpose...)
VIVID_SEQUENCE = [BLUE, RED, GREEN, AMBER, PURPLE, CYAN, PINK]

st.markdown(f"""
<style>
.section-title {{
    color: {NAVY};
    font-size: 20px;
    font-weight: 600;
    margin: 28px 0 4px 0;
}}
.insight-box {{
    background-color: {CARD_BG};
    border: 1px solid {CARD_BORDER};
    border-left: 4px solid {AMBER};
    border-radius: 8px;
    padding: 14px 18px;
    margin: 10px 0 20px 0;
    color: {NAVY};
    font-size: 14px;
}}
</style>
""", unsafe_allow_html=True)

PLOTLY_TEMPLATE = "plotly_white"


@st.cache_data
def load_data():
    return pd.read_csv("synthetic_loan_approval_dataset.csv")

df = load_data()


st.title("📊 Loan Portfolio Analysis")
st.caption("Exploratory analysis of the applicant dataset and the factors driving loan decisions")

st.write("")

# ============================================================
# 1. Loan status distribution (Donut chart)
# ============================================================
st.markdown('<div class="section-title">Loan status distribution</div>', unsafe_allow_html=True)

status_counts = df["Loan_Status"].value_counts().reset_index()
status_counts.columns = ["Loan_Status", "Count"]

fig_donut = px.pie(
    status_counts,
    names="Loan_Status",
    values="Count",
    hole=0.55,
    color="Loan_Status",
    color_discrete_map={"Approved": BLUE, "Rejected": RED},
    template=PLOTLY_TEMPLATE,
)
fig_donut.update_traces(textinfo="percent+label", textfont_size=13)
fig_donut.update_layout(showlegend=True, height=360, margin=dict(t=10, b=10, l=10, r=10))
st.plotly_chart(fig_donut, width="stretch")


# ============================================================
# 2. Missed payments: the clearest signal of all (very intuitive for clients)
# ============================================================
st.markdown('<div class="section-title">Approval rate by missed payments</div>', unsafe_allow_html=True)
st.caption("The single clearest pattern in the data: payment history dominates the decision")

df_mp = df.copy()
df_mp["Missed_Payments_Group"] = pd.cut(
    df_mp["Missed_Payments"],
    bins=[-1, 0, 2, 100],
    labels=["No missed payments", "1-2 missed payments", "3+ missed payments"],
)
mp_rate = (
    df_mp.groupby("Missed_Payments_Group", observed=True)["Loan_Status"]
    .apply(lambda x: (x == "Approved").mean() * 100)
    .reset_index()
)
mp_rate.columns = ["Group", "Approval_Rate"]

fig_mp = px.bar(
    mp_rate,
    x="Group",
    y="Approval_Rate",
    text_auto=".1f",
    template=PLOTLY_TEMPLATE,
    color="Group",
    color_discrete_sequence=[GREEN, AMBER, RED],
)
fig_mp.update_layout(
    height=360,
    margin=dict(t=10, b=10, l=10, r=10),
    xaxis_title="",
    yaxis_title="Approval rate (%)",
    showlegend=False,
)
st.plotly_chart(fig_mp, width="stretch")

st.markdown(f"""
<div class="insight-box">
<b>Key takeaway:</b> Applicants with no missed payments are approved 89% of the time.
That drops to 26% with 1-2 missed payments, and almost to zero (0.1%) with 3 or more —
payment history is the single strongest signal in the entire dataset.
</div>
""", unsafe_allow_html=True)


# ============================================================
# 3. Average debt-to-income by decision (replaces the box plot — simpler for clients)
# ============================================================
st.markdown('<div class="section-title">Debt-to-income ratio by decision</div>', unsafe_allow_html=True)
st.caption("Average share of income already committed to debt payments")

dti_avg = df.groupby("Loan_Status")["Debt_to_Income"].mean().reset_index()

fig_dti = px.bar(
    dti_avg,
    x="Loan_Status",
    y="Debt_to_Income",
    color="Loan_Status",
    color_discrete_map={"Approved": BLUE, "Rejected": RED},
    text_auto=".1f",
    template=PLOTLY_TEMPLATE,
)
fig_dti.update_layout(
    height=340,
    margin=dict(t=10, b=10, l=10, r=10),
    showlegend=False,
    xaxis_title="",
    yaxis_title="Average debt-to-income ratio (%)",
)
st.plotly_chart(fig_dti, width="stretch")

st.markdown(f"""
<div class="insight-box">
<b>Key takeaway:</b> Approved applicants carry an average debt-to-income ratio of just 9.3%,
compared to 53.0% for rejected applicants — a clear, easy-to-explain gap.
</div>
""", unsafe_allow_html=True)


# ============================================================
# 4. Credit score distribution by outcome
# ============================================================
st.markdown('<div class="section-title">Credit score distribution by outcome</div>', unsafe_allow_html=True)

fig_credit = px.histogram(
    df,
    x="Credit_Score",
    color="Loan_Status",
    barmode="overlay",
    opacity=0.75,
    nbins=40,
    color_discrete_map={"Approved": BLUE, "Rejected": RED},
    template=PLOTLY_TEMPLATE,
)
fig_credit.update_layout(
    height=380,
    margin=dict(t=10, b=10, l=10, r=10),
    xaxis_title="Credit score",
    yaxis_title="Number of applicants",
    legend_title="",
)
st.plotly_chart(fig_credit, width="stretch")


# ============================================================
# 5. Approval rate by employment type / city tier
# ============================================================
col_left, col_right = st.columns(2)

with col_left:
    st.markdown('<div class="section-title">Approval rate by employment type</div>', unsafe_allow_html=True)

    emp_rate = (
        df.groupby("Employment_Type")["Loan_Status"]
        .apply(lambda x: (x == "Approved").mean() * 100)
        .sort_values(ascending=True)
        .reset_index()
    )
    emp_rate.columns = ["Employment_Type", "Approval_Rate"]

    fig_emp = px.bar(
        emp_rate,
        x="Approval_Rate",
        y="Employment_Type",
        orientation="h",
        template=PLOTLY_TEMPLATE,
        text_auto=".1f",
        color="Employment_Type",
        color_discrete_sequence=VIVID_SEQUENCE,
    )
    fig_emp.update_layout(
        height=340,
        margin=dict(t=10, b=10, l=10, r=10),
        xaxis_title="Approval rate (%)",
        yaxis_title="",
        showlegend=False,
    )
    st.plotly_chart(fig_emp, width="stretch")

with col_right:
    st.markdown('<div class="section-title">Approval rate by loan purpose</div>', unsafe_allow_html=True)

    purpose_rate = (
        df.groupby("Loan_Purpose")["Loan_Status"]
        .apply(lambda x: (x == "Approved").mean() * 100)
        .sort_values(ascending=False)
        .reset_index()
    )
    purpose_rate.columns = ["Loan_Purpose", "Approval_Rate"]

    fig_purpose = px.bar(
        purpose_rate,
        x="Loan_Purpose",
        y="Approval_Rate",
        template=PLOTLY_TEMPLATE,
        text_auto=".1f",
        color="Loan_Purpose",
        color_discrete_sequence=VIVID_SEQUENCE,
    )
    fig_purpose.update_layout(
        height=340,
        margin=dict(t=10, b=10, l=10, r=10),
        xaxis_title="",
        yaxis_title="Approval rate (%)",
        showlegend=False,
    )
    st.plotly_chart(fig_purpose, width="stretch")


# ============================================================
# 6. Strongest factors behind the loan decision (correlation)
# ============================================================
st.markdown('<div class="section-title">Strongest factors behind the loan decision</div>', unsafe_allow_html=True)
st.caption("Correlation of each numeric feature with the final decision (Approved = 1)")

df_corr = df.copy()
df_corr["target"] = (df_corr["Loan_Status"] == "Approved").astype(int)
numeric_cols = df_corr.select_dtypes(include="number").columns.drop("target")
correlations = df_corr[numeric_cols].corrwith(df_corr["target"]).sort_values(key=abs)
correlations = correlations.tail(10)

fig_corr = go.Figure(go.Bar(
    x=correlations.values,
    y=correlations.index,
    orientation="h",
    marker_color=[GREEN if v > 0 else RED for v in correlations.values],
))
fig_corr.update_layout(
    template=PLOTLY_TEMPLATE,
    height=420,
    margin=dict(t=10, b=10, l=10, r=10),
    xaxis_title="Correlation with approval",
    yaxis_title="",
)
st.plotly_chart(fig_corr, width="stretch")


# ============================================================
# 7. Approval rate by number of existing loans
# ============================================================
st.markdown('<div class="section-title">Approval rate by number of existing loans</div>', unsafe_allow_html=True)
st.caption("Applicants already carrying more loans are approved far less often")

existing_loans_rate = (
    df.groupby("Existing_Loans")["Loan_Status"]
    .apply(lambda x: (x == "Approved").mean() * 100)
    .reset_index()
)
existing_loans_rate.columns = ["Existing_Loans", "Approval_Rate"]
existing_loans_rate["Existing_Loans"] = existing_loans_rate["Existing_Loans"].astype(str)

fig_existing = px.bar(
    existing_loans_rate,
    x="Existing_Loans",
    y="Approval_Rate",
    text_auto=".1f",
    template=PLOTLY_TEMPLATE,
    color_discrete_sequence=[BLUE],
)
fig_existing.update_layout(
    height=340,
    margin=dict(t=10, b=10, l=10, r=10),
    xaxis_title="Number of existing loans",
    yaxis_title="Approval rate (%)",
)
st.plotly_chart(fig_existing, width="stretch")

st.markdown(f"""
<div class="insight-box">
<b>Key takeaway:</b> Applicants with no existing loans are approved 90.8% of the time.
That drops sharply to 45.8% with just one existing loan, and keeps falling as the
number of existing loans increases — existing debt load is a major red flag.
</div>
""", unsafe_allow_html=True)


# ============================================================
# 8. Collateral impact
# ============================================================
col_a, col_b = st.columns(2)

with col_a:
    st.markdown('<div class="section-title">Approval rate by collateral</div>', unsafe_allow_html=True)

    collateral_rate = (
        df.groupby("Collateral")["Loan_Status"]
        .apply(lambda x: (x == "Approved").mean() * 100)
        .reset_index()
    )
    collateral_rate.columns = ["Collateral", "Approval_Rate"]

    fig_collateral = px.bar(
        collateral_rate,
        x="Collateral",
        y="Approval_Rate",
        text_auto=".1f",
        template=PLOTLY_TEMPLATE,
        color="Collateral",
        color_discrete_sequence=[GREEN, AMBER],
    )
    fig_collateral.update_layout(
        height=320,
        margin=dict(t=10, b=10, l=10, r=10),
        xaxis_title="",
        yaxis_title="Approval rate (%)",
        showlegend=False,
    )
    st.plotly_chart(fig_collateral, width="stretch")

with col_b:
    st.markdown('<div class="section-title">Applicant age distribution</div>', unsafe_allow_html=True)

    fig_age = px.histogram(
        df,
        x="Age",
        color="Loan_Status",
        barmode="overlay",
        opacity=0.75,
        nbins=30,
        color_discrete_map={"Approved": BLUE, "Rejected": RED},
        template=PLOTLY_TEMPLATE,
    )
    fig_age.update_layout(
        height=320,
        margin=dict(t=10, b=10, l=10, r=10),
        xaxis_title="Age",
        yaxis_title="Number of applicants",
        legend_title="",
    )
    st.plotly_chart(fig_age, width="stretch")


# ============================================================
# 9. Income vs Loan Amount scatter
# ============================================================
st.markdown('<div class="section-title">Monthly income vs loan amount</div>', unsafe_allow_html=True)
st.caption("Each point is one applicant, colored by the final decision")

scatter_sample = df.sample(min(2000, len(df)), random_state=42)

fig_scatter = px.scatter(
    scatter_sample,
    x="Monthly_Income",
    y="Loan_Amount",
    color="Loan_Status",
    opacity=0.5,
    color_discrete_map={"Approved": BLUE, "Rejected": RED},
    template=PLOTLY_TEMPLATE,
)
fig_scatter.update_layout(
    height=420,
    margin=dict(t=10, b=10, l=10, r=10),
    xaxis_title="Monthly income",
    yaxis_title="Loan amount",
    legend_title="",
)
st.plotly_chart(fig_scatter, width="stretch")


# ============================================================
# 10. Interactive explorer
# ============================================================
st.markdown('<div class="section-title">Explore applicants</div>', unsafe_allow_html=True)
st.caption("Filter the dataset to inspect specific applicant segments")

filter_col1, filter_col2 = st.columns(2)

with filter_col1:
    selected_employment = st.multiselect(
        "Employment type",
        options=sorted(df["Employment_Type"].unique()),
        default=sorted(df["Employment_Type"].unique()),
    )

with filter_col2:
    income_range = st.slider(
        "Monthly income range",
        min_value=int(df["Monthly_Income"].min()),
        max_value=int(df["Monthly_Income"].max()),
        value=(int(df["Monthly_Income"].min()), int(df["Monthly_Income"].max())),
    )

filtered_df = df[
    df["Employment_Type"].isin(selected_employment)
    & df["Monthly_Income"].between(income_range[0], income_range[1])
]

st.write(f"**{len(filtered_df):,}** applicants match this filter")

st.dataframe(
    filtered_df[[
        "Age", "Employment_Type", "Monthly_Income", "Credit_Score",
        "Debt_to_Income", "Loan_Amount", "Loan_Status"
    ]].head(50),
    width="stretch",
)