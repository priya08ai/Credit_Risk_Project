import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# ==================================================
# 1. PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Credit Risk Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# 2. CUSTOM DASHBOARD THEME
# ==================================================

st.markdown("""
<style>
.stApp {
    background-color: #F8F7F3;
}

[data-testid="stHeader"] {
    background-color: #F8F7F3;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

h1 {
    color: #245B45;
    font-weight: 800;
}

h2, h3 {
    color: #354B40;
}

p, label {
    color: #475569;
}

[data-testid="stMetric"] {
    background-color: #FFFFFF;
    border: 1px solid #E7E6DF;
    border-radius: 14px;
    padding: 18px;
    box-shadow: 0 3px 10px rgba(40, 60, 45, 0.06);
}

[data-testid="stMetricLabel"] {
    color: #64748B;
    font-size: 14px;
}

[data-testid="stMetricValue"] {
    color: #245B45;
    font-weight: 750;
}

[data-testid="stSidebar"] {
    background-color: #EDEFE8;
}

[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #245B45;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #FFFFFF;
    border: 1px solid #E7E6DF;
    border-radius: 14px;
    padding: 12px;
}

.stButton button {
    background-color: #287653;
    color: white;
    border-radius: 9px;
    border: none;
}

.stButton button:hover {
    background-color: #1E5D40;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# 3. LOAD DATASET
# ==================================================

@st.cache_data
def load_data():
    data = pd.read_csv("1-dataset/credit_risk_dataset.csv")
    return data

df = load_data()

# Create Age Groups
age_bins = [0, 25, 35, 45, 55, float("inf")]
age_labels = ["18-25", "26-35", "36-45", "46-55", "56+"]

df["age_group"] = pd.cut(
    df["person_age"],
    bins=age_bins,
    labels=age_labels,
    include_lowest=True
)

# ==================================================
# 4. DASHBOARD HEADER
# ==================================================

st.title("📊 CREDIT RISK ANALYTICS")
st.caption(
    "Customer Insights  |  Loan Performance  |  Default Risk Analysis"
)

st.divider()

# ==================================================
# 5. INTERACTIVE FILTERS
# ==================================================

st.sidebar.title("🎛️ Dashboard Controls")
st.sidebar.caption("Customize your analysis using filters.")

if st.sidebar.button("↻ Reset All Filters", use_container_width=True):
    st.session_state.clear()
    st.rerun()

age_options = [x for x in age_labels if x in df["age_group"].astype(str).unique()]

selected_age = st.sidebar.multiselect(
    "Age Group",
    age_options,
    default=age_options
)

grade_options = sorted(df["loan_grade"].dropna().unique())

selected_grade = st.sidebar.multiselect(
    "Loan Grade",
    grade_options,
    default=grade_options
)

purpose_options = sorted(df["loan_intent"].dropna().unique())

selected_purpose = st.sidebar.multiselect(
    "Loan Purpose",
    purpose_options,
    default=purpose_options
)

home_options = sorted(df["person_home_ownership"].dropna().unique())

selected_home = st.sidebar.multiselect(
    "Home Ownership",
    home_options,
    default=home_options
)

status_options = ["Non-Default", "Default"]

selected_status = st.sidebar.multiselect(
    "Loan Status",
    status_options,
    default=status_options
)

# ==================================================
# 6. APPLY FILTERS
# ==================================================

status_mapping = {
    "Non-Default": 0,
    "Default": 1
}

selected_status_values = [
    status_mapping[x] for x in selected_status
]

filtered_df = df[
    df["age_group"].astype(str).isin(selected_age) &
    df["loan_grade"].isin(selected_grade) &
    df["loan_intent"].isin(selected_purpose) &
    df["person_home_ownership"].isin(selected_home) &
    df["loan_status"].isin(selected_status_values)
].copy()

st.sidebar.divider()
st.sidebar.caption(
    f"Customers matching filters: {len(filtered_df):,}"
)

# ==================================================
# 7. KPI CARDS
# ==================================================

st.subheader("📌 Key Performance Indicators")

if filtered_df.empty:
    st.warning("No data found. Please change your filters.")
    st.stop()

total_customers = len(filtered_df)
total_loan = filtered_df["loan_amnt"].sum()
average_income = filtered_df["person_income"].mean()
average_interest = filtered_df["loan_int_rate"].mean()

default_customers = (
    filtered_df["loan_status"] == 1
).sum()

default_rate = (
    default_customers / total_customers * 100
)

k1, k2, k3 = st.columns(3)

k1.metric("👥 Total Customers", f"{total_customers:,}")
k2.metric("💰 Total Loan Amount", f"₹{total_loan:,.0f}")
k3.metric("💵 Average Income", f"₹{average_income:,.0f}")

k4, k5, k6 = st.columns(3)

k4.metric("📈 Average Interest Rate", f"{average_interest:.2f}%")
k5.metric("⚠️ Default Customers", f"{default_customers:,}")
k6.metric("📊 Default Rate", f"{default_rate:.2f}%")

st.divider()

# ==================================================
# COMMON CHART SETTINGS
# ==================================================

sns.set_theme(style="whitegrid")

def finish_chart(fig, ax):
    ax.set_facecolor("#FFFFFF")
    fig.patch.set_facecolor("#FFFFFF")
    ax.grid(axis="y", alpha=0.18)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

# ==================================================
# 8. AGE GROUP VS DEFAULT RATE
# ==================================================

st.subheader("📈 Age Group vs Default Rate")

age_rate = (
    filtered_df.groupby("age_group", observed=False)["loan_status"].mean() * 100
)

fig, ax = plt.subplots(figsize=(7, 4))

sns.barplot(
    x=age_rate.index.astype(str),
    y=age_rate.values,
    hue=age_rate.index.astype(str),
    palette="mako",
    legend=False,
    ax=ax
)

ax.set_xlabel("Age Group")
ax.set_ylabel("Default Rate (%)")
ax.set_title("Default Rate Across Age Groups")

finish_chart(fig, ax)

# ==================================================
# 9. INCOME VS DEFAULT RATE
# ==================================================

st.subheader("💵 Income vs Default Rate")

income_bins = [0, 25000, 50000, 75000, 100000, float("inf")]
income_labels = [
    "Below 25K",
    "25K-50K",
    "50K-75K",
    "75K-100K",
    "Above 100K"
]

filtered_df["income_group"] = pd.cut(
    filtered_df["person_income"],
    bins=income_bins,
    labels=income_labels,
    include_lowest=True
)

income_rate = (
    filtered_df.groupby("income_group", observed=False)["loan_status"].mean() * 100
)

fig, ax = plt.subplots(figsize=(7, 4))

sns.barplot(
    x=income_rate.index.astype(str),
    y=income_rate.values,
    hue=income_rate.index.astype(str),
    palette="crest",
    legend=False,
    ax=ax
)

ax.set_xlabel("Annual Income Group")
ax.set_ylabel("Default Rate (%)")
ax.set_title("Default Rate by Income")

finish_chart(fig, ax)

# ==================================================
# 10. LOAN PURPOSE DISTRIBUTION
# ==================================================

st.subheader("🎯 Loan Purpose Distribution")

purpose_count = filtered_df["loan_intent"].value_counts()

fig, ax = plt.subplots(figsize=(7, 4))

ax.pie(
    purpose_count.values,
    labels=purpose_count.index,
    autopct="%1.1f%%",
    startangle=90,
    colors=sns.color_palette("Set2", len(purpose_count)),
    wedgeprops={"width": 0.42, "edgecolor": "white"},
    textprops={"fontsize": 9}
)

ax.set_title("Customer Distribution by Loan Purpose")
finish_chart(fig, ax)

# ==================================================
# 11. LOAN GRADE DISTRIBUTION
# ==================================================

st.subheader("🏅 Loan Grade Distribution")

grade_count = filtered_df["loan_grade"].value_counts().sort_index()

fig, ax = plt.subplots(figsize=(7, 4))

sns.barplot(
    x=grade_count.index,
    y=grade_count.values,
    hue=grade_count.index,
    palette="flare",
    legend=False,
    ax=ax
)

ax.set_xlabel("Loan Grade")
ax.set_ylabel("Number of Customers")
ax.set_title("Customer Distribution by Loan Grade")

finish_chart(fig, ax)

# ==================================================
# 12. INTEREST RATE ANALYSIS
# ==================================================

st.subheader("📉 Interest Rate Analysis")

fig, ax = plt.subplots(figsize=(7, 4))

sns.histplot(
    data=filtered_df,
    x="loan_int_rate",
    hue="loan_status",
    bins=25,
    kde=True,
    palette={0: "#279B72", 1: "#E76F51"},
    ax=ax
)

ax.set_xlabel("Interest Rate (%)")
ax.set_ylabel("Number of Customers")
ax.set_title("Interest Rate Distribution by Loan Status")

finish_chart(fig, ax)

# ==================================================
# 13. HOME OWNERSHIP ANALYSIS
# ==================================================

st.subheader("🏠 Home Ownership Analysis")

home_count = filtered_df["person_home_ownership"].value_counts()

fig, ax = plt.subplots(figsize=(7, 4))

sns.barplot(
    x=home_count.index,
    y=home_count.values,
    hue=home_count.index,
    palette="pastel",
    legend=False,
    ax=ax
)

ax.set_xlabel("Home Ownership")
ax.set_ylabel("Number of Customers")
ax.set_title("Customers by Home Ownership")

finish_chart(fig, ax)

# ==================================================
# 14. LOAN AMOUNT DISTRIBUTION
# ==================================================

st.subheader("💰 Loan Amount Distribution")

fig, ax = plt.subplots(figsize=(7, 4))

sns.histplot(
    data=filtered_df,
    x="loan_amnt",
    bins=30,
    kde=True,
    color="#8A63B8",
    ax=ax
)

ax.set_xlabel("Loan Amount")
ax.set_ylabel("Number of Customers")
ax.set_title("Distribution of Loan Amount")

finish_chart(fig, ax)

# ==================================================
# 15. CORRELATION HEATMAP
# ==================================================

st.subheader("🔥 Correlation Heatmap")

numeric_df = filtered_df.select_dtypes(include="number")
correlation = numeric_df.corr()

fig, ax = plt.subplots(figsize=(10, 6))

sns.heatmap(
    correlation,
    annot=True,
    cmap="RdYlGn_r",
    fmt=".2f",
    linewidths=0.5,
    center=0,
    ax=ax
)

ax.set_title("Correlation Between Numerical Variables")

fig.tight_layout()
st.pyplot(fig, use_container_width=True)
plt.close(fig)

# ==================================================
# 16. DATA PREVIEW
# ==================================================

st.divider()

st.subheader("📋 Customer Data Preview")

with st.expander("View Filtered Customer Records"):
    st.dataframe(
        filtered_df,
        use_container_width=True,
        height=350
    )

st.success("Credit Risk Dashboard Loaded Successfully!")