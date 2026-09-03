import streamlit as st
import pandas as pd
import pickle


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Prediction",
    page_icon="📝",
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


# =========================================================
# COLORS
# =========================================================

NAVY = "#14304D"
TEXT_SECONDARY = "#6B7280"
CARD_BG = "#F7F8FA"
CARD_BORDER = "#E3E6EB"
BLUE = "#3B82F6"
RED = "#EF4444"
GREEN = "#22C55E"
AMBER = "#F59E0B"
PURPLE = "#8B5CF6"


# =========================================================
# CSS
# =========================================================

st.markdown(
    f"""
    <style>

    .header-banner {{
        background-color: {CARD_BG};
        border: 1px solid {CARD_BORDER};
        border-left: 5px solid {BLUE};
        border-radius: 10px;
        padding: 20px 24px;
        margin-bottom: 24px;
    }}

    .header-title {{
        color: {NAVY};
        font-size: 22px;
        font-weight: 700;
        margin-bottom: 6px;
    }}

    .header-desc {{
        color: {TEXT_SECONDARY};
        font-size: 14px;
    }}

    .section-header {{
        font-size: 16px;
        font-weight: 700;
        margin: 4px 0 14px 0;
        padding-bottom: 8px;
        border-bottom: 2px solid var(--accent);
        color: var(--accent);
    }}

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
    <div class="header-banner">

        <div class="header-title">
            🏦 Loan approval predictor
        </div>

        <div class="header-desc">
            Enter the applicant's personal, financial, and credit history
            details below to get an instant Approved / Rejected decision
            from our trained classification model.
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# LOAD MODEL
# =========================================================

@st.cache_resource
def load_model():

    with open("loan_approval_model.pkl", "rb") as f:
        model = pickle.load(f)

    return model


try:

    model = load_model()
    model_loaded = True

except Exception as e:

    model_loaded = False

    st.error(
        f"⚠️ Model could not be loaded: {e}"
    )


# =========================================================
# SECTION HEADER
# =========================================================

def section_header(icon, title, accent):

    st.markdown(
        f"""
        <div class="section-header"
             style="--accent: {accent};">
            {icon} {title}
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# INPUTS
# =========================================================

st.subheader("Applicant risk input parameters")

st.write("")

col1, col2, col3 = st.columns(3)


# =========================================================
# PERSONAL INFORMATION
# =========================================================

with col1:

    section_header(
        "👤",
        "Applicant demographics",
        BLUE
    )

    age = st.number_input(
        "Age",
        min_value=18,
        max_value=100,
        value=30
    )

    dependents = st.number_input(
        "Dependents",
        min_value=0,
        max_value=10,
        value=0
    )

    city_tier = st.selectbox(
        "City Tier",
        [1, 2, 3, 4]
    )

    years_current_job = st.number_input(
        "Years at Current Job",
        min_value=0,
        max_value=50,
        value=2
    )

    total_experience = st.number_input(
        "Total Work Experience",
        min_value=0,
        max_value=50,
        value=5
    )


# =========================================================
# FINANCIAL INFORMATION
# =========================================================

with col2:

    section_header(
        "💰",
        "Income & financial details",
        GREEN
    )

    monthly_income = st.number_input(
        "Monthly Income",
        min_value=0,
        value=15000
    )

    other_income = st.number_input(
        "Other Income",
        min_value=0,
        value=0
    )

    savings = st.number_input(
        "Savings",
        min_value=0,
        value=5000
    )

    investments = st.number_input(
        "Investments",
        min_value=0,
        value=0
    )

    bank_balance = st.number_input(
        "Bank Balance",
        min_value=0,
        value=2000
    )

    existing_loans = st.number_input(
        "Existing Loans",
        min_value=0,
        max_value=10,
        value=0
    )

    existing_loan_amount = st.number_input(
        "Existing Loan Amount",
        min_value=0,
        value=0
    )

    monthly_emi = st.number_input(
        "Monthly EMI",
        min_value=0,
        value=0
    )


# =========================================================
# CREDIT + LOAN INFORMATION
# =========================================================

with col3:

    section_header(
        "📊",
        "Credit history & loan details",
        PURPLE
    )

    credit_score = st.slider(
        "Credit Score",
        300,
        850,
        650
    )

    credit_utilization = st.slider(
        "Credit Card Utilization (%)",
        0,
        100,
        30
    )

    num_bank_accounts = st.number_input(
        "Number of Bank Accounts",
        min_value=0,
        max_value=10,
        value=1
    )

    num_credit_cards = st.number_input(
        "Number of Credit Cards",
        min_value=0,
        max_value=10,
        value=1
    )

    loan_defaults = st.number_input(
        "Loan Defaults",
        min_value=0,
        max_value=10,
        value=0
    )

    missed_payments = st.number_input(
        "Missed Payments",
        min_value=0,
        max_value=20,
        value=0
    )

    loan_amount = st.number_input(
        "Loan Amount",
        min_value=0,
        value=100000
    )

    loan_tenure = st.number_input(
        "Loan Tenure (months)",
        min_value=1,
        max_value=360,
        value=60
    )

    interest_rate = st.number_input(
        "Interest Rate (%)",
        min_value=0.0,
        max_value=50.0,
        value=10.0
    )


# =========================================================
# COLLATERAL
# =========================================================

st.write("")

section_header(
    "🏠",
    "Collateral",
    AMBER
)

col4, col5 = st.columns(2)


with col4:

    property_value = st.number_input(
        "Property Value",
        min_value=0,
        value=0
    )


with col5:

    collateral_value = st.number_input(
        "Collateral Value",
        min_value=0,
        value=0
    )


# =========================================================
# FEATURE ENGINEERING
# =========================================================

annual_income = monthly_income * 12

total_income = monthly_income + other_income

debt_to_income = (
    monthly_emi / monthly_income
    if monthly_income > 0
    else 0
)

loan_to_value = (
    loan_amount / collateral_value
    if collateral_value > 0
    else 0
)

loan_to_income = (
    loan_amount / annual_income
    if annual_income > 0
    else 0
)

emi_to_income = (
    monthly_emi / monthly_income
    if monthly_income > 0
    else 0
)

experience_ratio = (
    years_current_job / total_experience
    if total_experience > 0
    else 0
)

loan_burden = (
    (existing_loan_amount + loan_amount) / annual_income
    if annual_income > 0
    else 0
)


# =========================================================
# PREDICTION BUTTON
# =========================================================

st.write("")

_, btn_col, _ = st.columns([1, 1, 1])


with btn_col:

    predict_clicked = st.button(
        "⚡ Predict loan approval",
        type="primary",
        width="stretch",
        disabled=not model_loaded
    )


# =========================================================
# PREDICTION
# =========================================================

if predict_clicked:

    # -----------------------------------------------------
    # INPUT DATA
    # -----------------------------------------------------

    input_data = pd.DataFrame(
        [{
            "Age": age,
            "Dependents": dependents,
            "City_Tier": city_tier,
            "Years_at_Current_Job": years_current_job,
            "Total_Work_Experience": total_experience,

            "Monthly_Income": monthly_income,
            "Annual_Income": annual_income,
            "Other_Income": other_income,
            "Existing_Loans": existing_loans,
            "Existing_Loan_Amount": existing_loan_amount,
            "Monthly_EMI": monthly_emi,
            "Debt_to_Income": debt_to_income,

            "Savings": savings,
            "Investments": investments,
            "Bank_Balance": bank_balance,

            "Credit_Card_Utilization": credit_utilization,
            "Number_of_Bank_Accounts": num_bank_accounts,
            "Number_of_Credit_Cards": num_credit_cards,
            "Credit_Score": credit_score,
            "Loan_Defaults": loan_defaults,
            "Missed_Payments": missed_payments,

            "Loan_Amount": loan_amount,
            "Loan_Tenure": loan_tenure,
            "Interest_Rate": interest_rate,

            "Property_Value": property_value,
            "Collateral_Value": collateral_value,
            "Loan_to_Value": loan_to_value,

            "Total_Income": total_income,
            "Loan_to_Income": loan_to_income,
            "EMI_to_Income": emi_to_income,
            "Experience_Ratio": experience_ratio,
            "Loan_Burden": loan_burden,
        }]
    )


    # -----------------------------------------------------
    # MAKE SURE MODEL HAS PREDICT
    # -----------------------------------------------------

    if not hasattr(model, "predict"):

        st.error(
            "❌ The file loan_approval_model.pkl does not contain "
            "the trained ML Pipeline."
        )

        st.info(
            f"Loaded object type: {type(model)}"
        )

        st.warning(
            "Please save the trained Pipeline itself into "
            "loan_approval_model.pkl."
        )

        st.stop()


    # -----------------------------------------------------
    # PREDICTION
    # -----------------------------------------------------

    try:

        prediction = model.predict(input_data)[0]

    except Exception as e:

        st.error(
            "❌ Prediction failed."
        )

        st.exception(e)

        st.stop()


    # -----------------------------------------------------
    # PROBABILITY
    # -----------------------------------------------------

    confidence = None

    if hasattr(model, "predict_proba"):

        try:

            probabilities = model.predict_proba(input_data)[0]

            confidence = max(probabilities) * 100

        except Exception:

            confidence = None


    # -----------------------------------------------------
    # RESULT
    # -----------------------------------------------------

    st.write("")

    if prediction == "Approved":

        st.success(
            "✅ Decision: Loan Approved"
        )

    elif prediction == "Rejected":

        st.error(
            "❌ Decision: Loan Rejected"
        )

    else:

        st.warning(
            f"Prediction: {prediction}"
        )


    # -----------------------------------------------------
    # CONFIDENCE
    # -----------------------------------------------------

    if confidence is not None:

        st.write(
            f"Model confidence: **{confidence:.1f}%**"
        )
