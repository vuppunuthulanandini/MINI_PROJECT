

import streamlit as st
import pickle
import pandas as pd
import plotly.express as px
import numpy as np
import time

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Customer Intelligence", layout="wide")

# ---------------- UI ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #fdfbfb, #ebedee, #c2e9fb);
}
.title {
    text-align:center;
    font-size:45px;
    font-weight:bold;
}
.card {
    padding:20px;
    border-radius:15px;
    background:white;
    box-shadow:0px 5px 15px rgba(0,0,0,0.1);
    transition:0.3s;
}
.card:hover {
    transform:scale(1.05);
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD ----------------
model = pickle.load(open("models/churn_model.pkl","rb"))
columns = pickle.load(open("models/model_columns.pkl","rb"))

df = pd.read_csv("data/Customer-Churn.csv")
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors='coerce')
df.dropna(inplace=True)

# ---------------- STORY ----------------
def generate_story(features, prediction, prob):

    if prediction == 1:

        return f"""
This customer is likely drifting away with **{round(prob*100,2)}% risk**.

Factors like **{features}** suggest lower engagement.

👉 Offer discounts or better recommendations.
"""

    else:

        return f"""
This customer is stable with only **{round((1-prob)*100,2)}% risk**.

Strong engagement is observed.

👉 Maintain experience and reward loyalty.
"""

# ---------------- TITLE ----------------
st.markdown(
    '<div class="title">✨ Customer Intelligence</div>',
    unsafe_allow_html=True
)

# ---------------- SIDEBAR ----------------
role = st.sidebar.radio(
    "Mode",
    ["Customer","Admin"]
)

# =====================================================
# CUSTOMER UI
# =====================================================
if role == "Customer":

    st.subheader("🔍 Understand Customer Behavior")

    col1, col2 = st.columns(2)

    # ---------------- LEFT ----------------
    with col1:

        tenure = st.selectbox(
            "Tenure (Months)",
            options=list(range(1,25)),
            index=0,
            help="How long the customer has been using the service"
        )

        # CUSTOMER TYPE
        if tenure <= 6:
            st.warning("⚠️ New Customer (Higher churn risk)")

        elif tenure <= 15:
            st.info("🙂 Medium tenure customer")

        else:
            st.success("✅ Loyal Customer")

        monthly = st.number_input(
            "Monthly Charges"
        )

    # ---------------- RIGHT ----------------
    with col2:

        total = st.number_input(
            "Total Charges"
        )

        contract = st.selectbox(
            "Contract",
            ["Month-to-month","One year","Two year"]
        )

    # =====================================================
    # PREDICT
    # =====================================================
    if st.button("🚀 Predict"):

        with st.spinner("Analyzing..."):
            time.sleep(1)

        # CREATE EMPTY DATAFRAME
        data = pd.DataFrame(columns=columns)

        # FILL ALL VALUES WITH 0
        data.loc[0] = 0

        # ADD USER VALUES
        data["tenure"] = tenure
        data["MonthlyCharges"] = monthly
        data["TotalCharges"] = total

        # CONTRACT ENCODING
        if (
            "Contract_One year" in columns
            and contract == "One year"
        ):
            data["Contract_One year"] = 1

        if (
            "Contract_Two year" in columns
            and contract == "Two year"
        ):
            data["Contract_Two year"] = 1

        # ---------------- PREDICTION ----------------
        prediction = model.predict(data)[0]

        prob = model.predict_proba(data)[0][1]

        # ---------------- IMPORTANCE ----------------
        importance = pd.Series(
            model.coef_[0],
            index=columns
        )

        impact = data.iloc[0] * importance

        top = impact.sort_values(ascending=False)

        # =====================================================
        # REMOVE TECHNICAL FEATURES
        # =====================================================
        filtered_features = []

        for feature in top.index:

            feature_lower = feature.lower()

            if (
                "gender" not in feature_lower
                and
                "senior" not in feature_lower
                and
                "partner" not in feature_lower
                and
                "dependents" not in feature_lower
                and
                "paperless" not in feature_lower
            ):

                filtered_features.append(feature)

        # TAKE TOP 3
        top_features = filtered_features[:3]

        features = ", ".join(top_features)

        # ---------------- STORY ----------------
        story = generate_story(
            features,
            prediction,
            prob
        )

        # =====================================================
        # RESULT
        # =====================================================
        if prediction == 1:

            st.error(
                f"⚠️ High Risk — {round(prob*100,2)}%"
            )

        else:

            st.success(
                f"✅ Stable — {round((1-prob)*100,2)}%"
            )

        # =====================================================
        # PROGRESS BAR
        # =====================================================
        progress = st.progress(0)

        for i in range(int(prob*100)):

            progress.progress(i+1)

            time.sleep(0.01)

        # =====================================================
        # INSIGHTS
        # =====================================================
        st.markdown("### ✨ Key Insights")

        c1, c2, c3, c4 = st.columns(4)

        # RISK
        c1.markdown(
            f"""
<div class='card'>
<b>📊 Risk</b><br>
{round(prob*100,2)}%
</div>
""",
            unsafe_allow_html=True
        )

        # DRIVERS
        c2.markdown(
            f"""
<div class='card'>
<b>📉 Drivers</b><br>
{features}
</div>
""",
            unsafe_allow_html=True
        )

        # ACTION
        c3.markdown(
            """
<div class='card'>
<b>💡 Action</b><br>
Retention strategy
</div>
""",
            unsafe_allow_html=True
        )

        # INSIGHT
        insight = (
            "Low engagement"
            if prediction == 1
            else
            "Healthy usage"
        )

        c4.markdown(
            f"""
<div class='card'>
<b>🧠 Insight</b><br>
{insight}
</div>
""",
            unsafe_allow_html=True
        )

        # STORY
        st.markdown(
            f"<div class='card'>{story}</div>",
            unsafe_allow_html=True
        )

# =====================================================
# ADMIN UI
# =====================================================
else:

    st.subheader("📊 Advanced Admin Dashboard")

    total = len(df)

    churn = df[df["Churn"]=="Yes"].shape[0]

    churn_rate = round(
        (churn/total)*100,
        2
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Users",
        total
    )

    col2.metric(
        "Churned Users",
        churn
    )

    col3.metric(
        "Churn %",
        churn_rate
    )

    st.markdown("---")

    # =====================================================
    # CHARTS
    # =====================================================
    col1, col2 = st.columns(2)

    with col1:

        st.plotly_chart(
            px.pie(
                df,
                names="Churn"
            ),
            use_container_width=True
        )

    with col2:

        st.plotly_chart(
            px.box(
                df,
                x="Churn",
                y="MonthlyCharges"
            ),
            use_container_width=True
        )

    st.plotly_chart(
        px.histogram(
            df,
            x="tenure",
            color="Churn"
        ),
        use_container_width=True
    )

    # =====================================================
    # INSIGHTS
    # =====================================================
    st.subheader("🔥 Key Insights")

    avg_tenure = df["tenure"].mean()

    avg_monthly = df["MonthlyCharges"].mean()

    st.info(
        f"📌 Average tenure: {round(avg_tenure,1)} months"
    )

    st.info(
        f"📌 Average monthly charges: ₹{round(avg_monthly,2)}"
    )

    high_churn_segment = df[df["tenure"] < 6].shape[0]

    if high_churn_segment > total * 0.3:

        st.error(
            "⚠️ Many new users are churning early"
        )

    if churn_rate > 20:

        st.error(
            "⚠️ Overall churn rate is high"
        )

    # =====================================================
    # ACTIONS
    # =====================================================
    st.subheader("💡 Recommended Actions")

    if churn_rate > 15:

        st.success(
            "👉 Provide discounts for new users"
        )

    if avg_tenure < 12:

        st.success(
            "👉 Improve onboarding experience"
        )

    if avg_monthly > 70:

        st.success(
            "👉 Optimize pricing strategy"
        )