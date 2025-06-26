from datetime import date, timedelta
import streamlit as st
import pandas as pd

#here will be some function to process assets from qm system, obtain their type and date

#fake data (organized as dict of dicts):
June2025= {"Week 1": {"images": 120, "videos": 45, "audio": 35, "documents": 65},
        "Week 2": {"images": 95, "videos": 60, "audio": 25, "documents": 70},
        "Week 3": {"images": 62, "videos": 91, "audio": 40, "documents": 48},
        "Week 4": {"images": 99, "videos": 23, "audio": 42, "documents": 89}}



st.write("Digital Assets Dashboard")


week = st.button("Weekly View")
month = st.button("Monthly View")

today = date.today() #current time period + week
start_of_week = today - timedelta(days=today.weekday())
end_of_week = start_of_week + timedelta(days=6)



if week:
    st.write(f"Viewing: Week of {start_of_week} to {end_of_week}") 

if month:
    st.write("Viewing: June 2025")
    month_data = {"images": 0, "videos": 0, "audio": 0, "documents": 0}
    for week_data in June2025.values(): #goes through june2025 data, adding up monthly values
        for type, numberOfType in week_data.items():
            month_data[type] += numberOfType



    assetsCount = month_data.values()
    totalAssets = 0; #counting up total number of assets for month
    for count in assetsCount:
        totalAssets+=count;
    st.title(f"Total Assets:  {totalAssets}") 



    split_dicts = [{k: v} for k, v in month_data.items()] #splitting monthdata into indicidual dicts
    for indiv_dict in split_dicts:
        df = pd.DataFrame(indiv_dict, index=['0']) #putting them into individual bar charts
        st.bar_chart(df)




















