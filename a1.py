import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
from streamlit_gsheets import GSheetsConnection
import random       
import time         

# Set Seaborn theme for better aesthetics
sns.set_theme(style="whitegrid")
plt.rcParams.update({'font.size': 12})

# Google Sheets connection
url = "https://docs.google.com/spreadsheets/d/1nnFGEIlgS6zJ8MR_QYfpGlSizvfcB1PEC8CvJ426Hms/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)
data = conn.read(spreadsheet=url)

if "chart_shown" not in st.session_state:
    st.session_state.chart_shown = False
if "chart_type" not in st.session_state:
    st.session_state.chart_type = None
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "end_time" not in st.session_state:
    st.session_state.end_time = None

st.title("Diamond's cut identification A/B test")
st.write("**Question:** Which diamond **cut** has the highest average price?")

def plot_chart_a():
    st.write("**Chart A: Bar Plot** of average price by cut")
    fig, ax = plt.subplots()
    avg_price_by_cut = data.groupby("cut")["price"].mean().reset_index()
    ax.bar(avg_price_by_cut["cut"], avg_price_by_cut["price"])
    ax.set_xlabel("Cut")
    ax.set_ylabel("Average Price")
    ax.set_title("Average Diamond Price by Cut (Bar Chart)")
    st.pyplot(fig)

def plot_chart_b():
    st.write("**Chart B: Box Plot** of price by cut")
    fig, ax = plt.subplots()
    sns.boxplot(x="cut", y="price", data=data, ax=ax)
    ax.set_title("Distribution of Diamond Price by Cut (Box Plot)")
    st.pyplot(fig)

if st.button("Show me a random chart"):
    st.session_state.chart_shown = True
    st.session_state.chart_type = random.choice(["A", "B"])
    st.session_state.start_time = time.time()

if st.session_state.chart_shown:
    if st.session_state.chart_type == "A":
        plot_chart_a()
    else:
        plot_chart_b()
    
    if st.button("I answered your question"):
        st.session_state.end_time = time.time()
        duration = st.session_state.end_time - st.session_state.start_time
        st.write(f"It took you **{duration:.2f} seconds** to answer the question. Thank you!")
