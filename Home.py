import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Loan Approval System",
    page_icon="🏦",
    layout="wide"
)


@st.cache_data
def load_data():
    return pd.read_csv("synthetic_loan_approval_dataset.csv")

df = load_data()

# ---------- محسوبات إحصائية حقيقية من الداتا ----------
total_applications = len(df)
approval_rate = (df["Loan_Status"] == "Approved").mean() * 100
avg_interest_rate = df["Interest_Rate"].mean()
avg_loan_amount = df["Loan_Amount"].mean()
avg_credit_score = df["Credit_Score"].mean()
approved_count = (df["Loan_Status"] == "Approved").sum()
rejected_count = (df["Loan_Status"] == "Rejected").sum()

approval_by_purpose = (
    df.groupby("Loan_Purpose")["Loan_Status"]
    .apply(lambda x: (x == "Approved").mean() * 100)
    .sort_values(ascending=False)
)

# ---------- لوحة ألوان حيوية، كل كارت بلونه المميز (نفس فكرة الـ Reference) ----------
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

st.markdown(f"""
<style>
.stat-card {{
    background-color: {CARD_BG};
    border: 1px solid {CARD_BORDER};
    border-left: 4px solid var(--accent);
    border-radius: 10px;
    padding: 18px 16px;
}}
.stat-label {{
    color: {TEXT_SECONDARY};
    font-size: 12px;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    margin-bottom: 8px;
}}
.stat-value {{
    color: {NAVY};
    font-size: 26px;
    font-weight: 700;
    margin-bottom: 4px;
}}
.stat-sub {{
    font-size: 12px;
    font-weight: 600;
    color: var(--accent);
}}
.section-title {{
    color: {NAVY};
    font-size: 20px;
    font-weight: 600;
    margin: 32px 0 4px 0;
}}
.purpose-card {{
    background-color: {CARD_BG};
    border: 1px solid {CARD_BORDER};
    border-left: 4px solid {AMBER};
    border-radius: 8px;
    padding: 14px 20px;
    margin-bottom: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}}
.purpose-name {{
    color: {NAVY};
    font-size: 15px;
    font-weight: 500;
}}
.purpose-rate {{
    color: {AMBER};
    font-size: 17px;
    font-weight: 700;
}}
</style>
""", unsafe_allow_html=True)


def stat_card(label, value, sub, accent):
    # فانكشن مساعدة عشان منكررش نفس الـ HTML 7 مرات — بس بنغيّر اللون (accent) لكل كارت
    st.markdown(f"""
    <div class="stat-card" style="--accent: {accent};">
        <div class="stat-label">{label}</div>
        <div class="stat-value">{value}</div>
        <div class="stat-sub">{sub}</div>
    </div>
    """, unsafe_allow_html=True)


# ---------- Header ----------
st.title("🏦 Loan Approval System")
st.caption("Machine learning-powered credit risk assessment and loan decision support")

st.write("")

# ---------- صف الكروت الرئيسية (KPIs) - كل كارت بلون مختلف ----------
k1, k2, k3, k4 = st.columns(4)
with k1:
    stat_card("Total Applications", f"{total_applications:,}", "Active dataset records", BLUE)
with k2:
    stat_card("Approval Rate", f"{approval_rate:.1f}%", f"{approved_count:,} approved", GREEN)
with k3:
    stat_card("Avg Interest Rate", f"{avg_interest_rate:.1f}%", "Across all loans", AMBER)
with k4:
    stat_card("Avg Credit Score", f"{avg_credit_score:.0f}", "Applicant average", PURPLE)

st.write("")

k5, k6, k7 = st.columns(3)
with k5:
    stat_card("Avg Loan Amount", f"${avg_loan_amount:,.0f}", "Per application", CYAN)
with k6:
    stat_card("Approved Loans", f"{approved_count:,}", "Successful applications", GREEN)
with k7:
    stat_card("Rejected Loans", f"{rejected_count:,}", "Declined applications", RED)


# ---------- قسم: نسبة الموافقة حسب المستوى التعليمي ----------
st.markdown('<div class="section-title">Approval rate by loan purpose</div>', unsafe_allow_html=True)
st.caption("How likely an application is to be approved, based on why the applicant is borrowing")

for purpose, rate in approval_by_purpose.items():
    st.markdown(f"""
    <div class="purpose-card">
        <span class="purpose-name">{purpose}</span>
        <span class="purpose-rate">{rate:.1f}%</span>
    </div>
    """, unsafe_allow_html=True)


# ---------- التنقل ----------
st.write("")
st.markdown('<div class="section-title">Explore the app</div>', unsafe_allow_html=True)
st.markdown("""
Use the sidebar to navigate:
- **Analysis** — deeper exploration of the dataset, distributions, and feature relationships.
- **Prediction** — enter a new applicant's details and get an instant Approved/Rejected decision.
""")