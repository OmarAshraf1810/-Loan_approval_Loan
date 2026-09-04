import streamlit as st
import pandas as pd
import joblib


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Loan Prediction",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# LOAD MODEL
# =========================================================

@st.cache_resource
def load_model():
    return joblib.load("loan_approval_model.pkl")


try:
    model = load_model()
    model_loaded = True

except Exception as e:
    model_loaded = False
    st.error(f"Model could not be loaded: {e}")


# =========================================================
# TITLE
# =========================================================

st.title("🏦 Loan Approval Prediction")

st.write(
    "Enter the applicant information and click Predict "
    "to get the decision from the trained machine learning model."
)


# =========================================================
# PERSONAL INFORMATION
# =========================================================

st.subheader("👤 Personal Information")

col1, col2, col3 = st.columns(3)

with col1:

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

    gender = st.selectbox(
        "Gender",
        [
            "Male",
            "Female",
            "Others"
        ]
    )


with col2:

    marital_status = st.selectbox(
        "Marital Status",
        [
            "Single",
            "Married",
            "Widowed",
            "Divorced"
        ]
    )

    education = st.selectbox(
        "Education",
        [
            "Graduate",
            "Post Graduate",
            "PhD",
            "High School",
            "Diploma",
            "No Formal"
        ]
    )

    residence_type = st.selectbox(
        "Residence Type",
        [
            "Rural",
            "Urban"
        ]
    )


with col3:

    city_tier = st.selectbox(
        "City Tier",
        [1, 2, 3, 4]
    )

    years_current_job = st.number_input(
        "Years at Current Job",
        min_value=0,
        max_value=50,
        value=3
    )

    total_experience = st.number_input(
        "Total Work Experience",
        min_value=0,
        max_value=50,
        value=5
    )


# =========================================================
# EMPLOYMENT & INCOME
# =========================================================

st.subheader("💼 Employment & Income")

col1, col2, col3 = st.columns(3)

with col1:

    employment_type = st.selectbox(
        "Employment Type",
        [
            "Private",
            "Government",
            "Self-Employed",
            "Unemployed",
            "Skilled Labor"
        ]
    )


with col2:

    monthly_income = st.number_input(
        "Monthly Income",
        min_value=0.0,
        value=50000.0,
        step=1000.0
    )


with col3:

    annual_income = st.number_input(
        "Annual Income",
        min_value=0.0,
        value=600000.0,
        step=10000.0
    )


other_income = st.number_input(
    "Other Income",
    min_value=0.0,
    value=0.0,
    step=1000.0
)


# =========================================================
# FINANCIAL INFORMATION
# =========================================================

st.subheader("💰 Financial Information")

col1, col2, col3 = st.columns(3)

with col1:

    savings = st.number_input(
        "Savings",
        min_value=0.0,
        value=100000.0,
        step=5000.0
    )

    investments = st.number_input(
        "Investments",
        min_value=0.0,
        value=20000.0,
        step=5000.0
    )


with col2:

    bank_balance = st.number_input(
        "Bank Balance",
        min_value=0.0,
        value=30000.0,
        step=5000.0
    )

    existing_loans = st.number_input(
        "Existing Loans",
        min_value=0,
        max_value=20,
        value=0
    )


with col3:

    existing_loan_amount = st.number_input(
        "Existing Loan Amount",
        min_value=0.0,
        value=0.0,
        step=5000.0
    )

    monthly_emi = st.number_input(
        "Monthly EMI",
        min_value=0.0,
        value=3000.0,
        step=500.0
    )


# =========================================================
# CREDIT INFORMATION
# =========================================================

st.subheader("📊 Credit Information")

col1, col2, col3 = st.columns(3)

with col1:

    credit_score = st.slider(
        "Credit Score",
        min_value=300,
        max_value=850,
        value=750
    )

    credit_utilization = st.number_input(
        "Credit Card Utilization (%)",
        min_value=0.0,
        max_value=100.0,
        value=20.0,
        step=1.0
    )


with col2:

    num_bank_accounts = st.number_input(
        "Number of Bank Accounts",
        min_value=0,
        max_value=20,
        value=2
    )

    num_credit_cards = st.number_input(
        "Number of Credit Cards",
        min_value=0,
        max_value=20,
        value=2
    )


with col3:

    loan_defaults = st.number_input(
        "Loan Defaults",
        min_value=0,
        max_value=20,
        value=0
    )

    missed_payments = st.number_input(
        "Missed Payments",
        min_value=0,
        max_value=30,
        value=0
    )


# =========================================================
# VERIFICATION
# =========================================================

st.subheader("✅ Verification")

col1, col2, col3 = st.columns(3)

with col1:

    tax_return = st.selectbox(
        "Tax Return Filed",
        ["Yes", "No"]
    )


with col2:

    pan_verified = st.selectbox(
        "PAN Verified",
        ["Yes", "No"]
    )


with col3:

    aadhaar_verified = st.selectbox(
        "Aadhaar Verified",
        ["Yes", "No"]
    )


# =========================================================
# LOAN INFORMATION
# =========================================================

st.subheader("🏦 Loan Information")

col1, col2, col3 = st.columns(3)

with col1:

    loan_amount = st.number_input(
        "Loan Amount",
        min_value=0.0,
        value=100000.0,
        step=5000.0
    )

    loan_tenure = st.number_input(
        "Loan Tenure (Months)",
        min_value=1,
        max_value=360,
        value=60
    )


with col2:

    interest_rate = st.number_input(
        "Interest Rate (%)",
        min_value=0.0,
        max_value=50.0,
        value=8.0,
        step=0.1
    )

    loan_purpose = st.selectbox(
        "Loan Purpose",
        [
            "Personal",
            "Home",
            "Education",
            "Vehicle",
            "Business",
            "Medical"
        ]
    )


with col3:

    collateral = st.selectbox(
        "Collateral",
        [
            "Yes",
            "No"
        ]
    )

    property_value = st.number_input(
        "Property Value",
        min_value=0.0,
        value=300000.0,
        step=10000.0
    )

    collateral_value = st.number_input(
        "Collateral Value",
        min_value=0.0,
        value=200000.0,
        step=10000.0
    )


# =========================================================
# FEATURE ENGINEERING
# =========================================================

# These engineered features must match the training logic.

total_income = (
    annual_income +
    (other_income * 12)
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
    total_experience / age
    if age > 0
    else 0
)


loan_burden = (
    (existing_loan_amount + loan_amount)
    / annual_income
    if annual_income > 0
    else 0
)


# Raw dataset features
# are represented as percentages.

debt_to_income = (
    (monthly_emi / monthly_income) * 100
    if monthly_income > 0
    else 0
)


loan_to_value = (
    (loan_amount / collateral_value) * 100
    if collateral_value > 0
    else 0
)


# =========================================================
# PREDICT BUTTON
# =========================================================

st.write("")

predict_clicked = st.button(
    "⚡ Predict Loan Approval",
    type="primary",
    use_container_width=True,
    disabled=not model_loaded
)


# =========================================================
# MODEL PREDICTION
# =========================================================

if predict_clicked:

    # -----------------------------------------------------
    # Create ONE applicant row
    # -----------------------------------------------------

    input_data = pd.DataFrame(
        [{
            "Age": age,
            "Gender": gender,
            "Marital_Status": marital_status,
            "Education": education,
            "Dependents": dependents,
            "Residence_Type": residence_type,

            "City_Tier": city_tier,
            "Employment_Type": employment_type,
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

            "Tax_Return_Filed": tax_return,
            "PAN_Verified": pan_verified,
            "Aadhaar_Verified": aadhaar_verified,

            "Loan_Purpose": loan_purpose,
            "Loan_Amount": loan_amount,
            "Loan_Tenure": loan_tenure,
            "Interest_Rate": interest_rate,

            "Property_Value": property_value,
            "Collateral_Value": collateral_value,
            "Collateral": collateral,
            "Loan_to_Value": loan_to_value,

            "Total_Income": total_income,
            "Loan_to_Income": loan_to_income,
            "EMI_to_Income": emi_to_income,
            "Experience_Ratio": experience_ratio,
            "Loan_Burden": loan_burden
        }]
    )


    # -----------------------------------------------------
    # IMPORTANT:
    # THE MODEL MAKES THE DECISION
    # -----------------------------------------------------

    try:

        prediction = model.predict(input_data)[0]

    except Exception as e:

        st.error("❌ Prediction failed.")

        st.exception(e)

        st.stop()


    # =====================================================
    # RESULT
    # =====================================================

    st.write("")

    # -----------------------------------------------------
    # APPROVED
    # -----------------------------------------------------

    if prediction == 1:

        st.success(
            "✅ LOAN APPROVED"
        )


    # -----------------------------------------------------
    # REJECTED
    # -----------------------------------------------------

    elif prediction == 0:

        st.error(
            "❌ LOAN REJECTED"
        )

        st.write("### Possible Reasons:")

        reasons = []


        if credit_score < 600:
            reasons.append(
                "Low Credit Score"
            )


        if missed_payments > 2:
            reasons.append(
                "High Number of Missed Payments"
            )


        if loan_defaults > 0:
            reasons.append(
                "Previous Loan Defaults"
            )


        if debt_to_income > 40:
            reasons.append(
                "High Debt-to-Income Ratio"
            )


        if loan_to_income > 0.5:
            reasons.append(
                "Loan Amount is High Compared with Annual Income"
            )


        if loan_to_value > 80:
            reasons.append(
                "High Loan-to-Value Ratio"
            )


        if existing_loans >= 3:
            reasons.append(
                "High Number of Existing Loans"
            )


        if credit_utilization > 70:
            reasons.append(
                "High Credit Card Utilization"
            )


        if savings < loan_amount * 0.1:
            reasons.append(
                "Low Savings Compared with Requested Loan"
            )


        if pan_verified == "No":
            reasons.append(
                "PAN is Not Verified"
            )


        if aadhaar_verified == "No":
            reasons.append(
                "Aadhaar is Not Verified"
            )


        if tax_return == "No":
            reasons.append(
                "Tax Return Has Not Been Filed"
            )


        if len(reasons) == 0:

            st.info(
                "The model rejected the application based "
                "on the overall combination of the applicant's features."
            )

        else:

            for reason in reasons:

                st.write(
                    f"🔴 {reason}"
                )


    # -----------------------------------------------------
    # UNEXPECTED MODEL OUTPUT
    # -----------------------------------------------------

    else:

        st.warning(
            f"Unexpected model output: {prediction}"
        )