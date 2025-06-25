import streamlit as st






st.write("Hello world")
st.write("Digital Assets Dashboard")


week = st.button("Weekly View")
month = st.button("Monthly View")

if week:
    st.write("Viewing: Week of June 2-8, 2025")

if month:
    st.write("Viewing: June 2025")

totalAssets = 5000
st.title(f"Total Assets:  {totalAssets}")
















