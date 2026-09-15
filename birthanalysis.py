import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page Configuration

st.set_page_config(
    page_title="Birth Data Analysis",
    layout="wide"
)

# Load Dataset

dataset = pd.read_csv("births.csv")

# Data Preprocessing

yearly_births = dataset.pivot_table(
    index="year",
    columns="gender",
    values="births",
    aggfunc="sum"
).reset_index()

yearly_births["total_births"] = (
    yearly_births["F"] + yearly_births["M"]
)

yearly_births["difference_in_births"] = (
    yearly_births["M"] - yearly_births["F"]
)

yearly_births["std_dev"] = yearly_births[["F", "M"]].std(axis=1)


# Dashboard Title

st.title("Birth Data Analysis Dashboard")
st.caption("Analysis of yearly male and female birth statistics")

st.divider()


# Key Metrics

total_births = dataset["births"].sum()
male_births = dataset.loc[dataset["gender"] == "M", "births"].sum()
female_births = dataset.loc[dataset["gender"] == "F", "births"].sum()
total_years = dataset["year"].nunique()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Births", f"{total_births:,}")
col2.metric("Male Births", f"{male_births:,}")
col3.metric("Female Births", f"{female_births:,}")
col4.metric("Years", total_years)

st.divider()


# Year Filter

st.subheader("🔎 Filter by Year")

min_year = int(dataset["year"].min())
max_year = int(dataset["year"].max())

selected_year = st.slider(
    "Select Year",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

filtered_data = yearly_births[
    (yearly_births["year"] >= selected_year[0]) &
    (yearly_births["year"] <= selected_year[1])
]

# Male vs Female Births

st.subheader("📈 Male vs Female Births by Year")

fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(
    filtered_data["year"],
    filtered_data["F"],
    marker="o",
    label="Female"
)

ax.plot(
    filtered_data["year"],
    filtered_data["M"],
    marker="o",
    label="Male"
)

ax.set_xlabel("Year")
ax.set_ylabel("Number of Births")
ax.set_title("Yearly Male and Female Births")
ax.legend()
ax.grid(True)

st.pyplot(fig)

# -----------------------------
# Total Births Chart
# -----------------------------
st.subheader("📊 Total Births by Year")

fig2, ax2 = plt.subplots(figsize=(10, 5))

ax2.bar(
    filtered_data["year"],
    filtered_data["total_births"]
)

ax2.set_xlabel("Year")
ax2.set_ylabel("Total Births")
ax2.set_title("Total Births by Year")

st.pyplot(fig2)

# Statistics

st.subheader("📋 Statistical Summary")

st.dataframe(
    filtered_data.describe(),
    use_container_width=True
)

# Processed Data

st.subheader("📑 Processed Birth Data")

st.dataframe(
    filtered_data,
    use_container_width=True
)