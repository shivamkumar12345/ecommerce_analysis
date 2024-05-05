import streamlit as st
import pandas as pd
import plotly.express as px
import os
import datetime
st.title("My Dashboard")

# file = st.file_uploader("Upload file",type=({"csv","xlsx"}))

# dir = os.chdir(r"C:\Users\DELL\Desktop")
# if file is not None:
#     st.write("Selected file Name: " + file.name)
#     df= pd.read_csv(file.name,encoding="ISO-8859-1")
#     st.write(df)
# else:
df= pd.read_csv(r"https://github.com/shivamkumar12345/ecommerce_analysis/blob/main/Superstore.csv",encoding="ISO-8859-1")
st.write(df)

# col1,col2 = st.columns(2)

# df["Order Date"] = pd.to_datetime(df["Order Date"],format='mixed')

# date1 =pd.to_datetime(df["Order Date"]).min()
# date2 = pd.to_datetime(df["Order Date"]).min()
# st.write(date1)
# st.write(date2)
# with col1:
#     startTime = pd.to_datetime(st.date_input("Start date"),date1)

# with col2:
#     endTime = pd.to_datetime(st.date_input("End date"),date2)

fig= px.bar(df.head(20),x='Region', y="Sales",color='Category',width=700)
st.plotly_chart(fig)

fig= px.bar(df.head(50),x='City', y="Sales",color='Profit',hover_data=['Category'],width=700,title="Sales in region with highest profit")
st.plotly_chart(fig)

fig =px.pie(df,names='Sub-Category',values='Profit',title="Order Count of Categories Sub-Catagory")
st.plotly_chart(fig)