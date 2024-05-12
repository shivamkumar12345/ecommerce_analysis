import streamlit as st
import pandas as pd
import plotly.express as px
import os
import datetime
st.title("My Dashboard")

def load_file(path):
    if file is not None:
        st.write("Selected file Name: " + file.name)

        ext = str(path.name).split(".")[-1]
        if(ext == 'csv'):
            df= pd.read_csv(path,encoding="ISO-8859-1")
        elif ext == 'xlsx':
            df = pd.read_excel(path)
        return df
    else:
        df= pd.read_csv(r"Superstore.csv",encoding="ISO-8859-1")
        return df

file = st.file_uploader("Upload file",type=({"csv","xlsx"}))


df= load_file(file)

with st.expander("open uploaded file"):
    st.write(df)

col1,col2 = st.columns((2))

df["Order Date"] = pd.to_datetime(df["Order Date"],format='mixed')

date1 =pd.to_datetime(df["Order Date"]).min()
date2 = pd.to_datetime(df["Order Date"]).max()

with col1:
    startTime = pd.to_datetime(st.date_input("Start date",date1))

with col2:
    endTime = pd.to_datetime(st.date_input("End date",date2))

df= df[(df["Order Date"]>=startTime) & (df["Order Date"] <= endTime)].copy()

# st.write(df)

#side bar
st.sidebar.header("side bar")

region = st.sidebar.multiselect("Select Region",df["Region"].unique())


state = st.sidebar.multiselect("Select State",df["State"].unique())

city = st.sidebar.multiselect("Select City",df["City"].unique())


#filter data through multiselect options
if not region and not state  and not city:
    filtered_df = df
elif not state and not city:
    filtered_df = df[df["Region"].isin(region)]

elif not region and not city:
    filtered_df = df[df["State"].isin(state)]

elif not region and not state:
    filtered_df = df[df["City"].isin(city)]

elif region and state:
    filtered_df = df[(df["Region"].isin(region)) & (df["State"].isin(state))]

elif region and city:
    filtered_df = df[(df["Region"].isin(region)) & (df["City"].isin(city))]

elif city and state:
    filtered_df = df[(df["City"].isin(city)) & (df["State"].isin(state))]

else:
    filtered_df = df[(df["City"].isin(city)) & (df["State"].isin(state)) & (df["Region"].isin(region))]




#plot graph of sales
category_sales = filtered_df.groupby(by="Category",as_index=False)["Sales"].sum()



with col1:
    fig= px.bar(category_sales,x="Category", y="Sales",title="plot b/w Category and sales")
    st.plotly_chart(fig,use_container_width=True)
with col2:
    fig= px.pie(filtered_df,names="Region", values="Sales",title="plot b/w Region and sales")
    st.plotly_chart(fig,use_container_width=True)

cl1,cl2 = st.columns((2))

#show data of filtered_df
with cl1:
    with st.expander("show region wise sales"):
        region_sales = filtered_df.groupby(by="Region",as_index=False)["Sales"].sum()
        st.write(region_sales.style.background_gradient(cmap="Blues"))

        csv= region_sales.to_csv().encode("utf-8")
        st.download_button("Download csv",data=csv,file_name="region_sales.csv",mime="text/csv" )

with cl2:
    with st.expander("show category wise sales"):
        st.write(category_sales.style.background_gradient(cmap="pink"))
        
        csv= category_sales.to_csv().encode("utf-8")
        st.download_button("Download csv",data=csv,file_name="Category_sales.csv",mime="text/csv")


#graph of monthly wise sales
filtered_df["month_year"] = filtered_df["Order Date"].dt.strftime("%Y : %b")

newCsv = filtered_df.groupby(by="month_year",as_index=False)["Sales"].sum()

with st.expander("monthly sales csv"):
    st.write(newCsv.T.style.background_gradient("pink"))

st.subheader("Month wise sales analysis")
fig= px.line(newCsv,x="month_year",y="Sales")
st.plotly_chart(fig,use_container_width=True,height=500)
# st.write(filtered_df)

#tree map b/w region, category, sub-category
fig= px.treemap(filtered_df,path=['Region',"Category","Sub-Category"],values="Sales",color='Sub-Category')
st.plotly_chart(fig,use_container_width=True)

# bar graph b/w region and sales
fig= px.bar(filtered_df,x='Region', y="Sales",color='Category',width=700,title="plot of region sales")
st.plotly_chart(fig,use_container_width=True)

#scatter plot b/w sales and profit
fig= px.scatter(filtered_df, x="Sales", y="Profit",size="Quantity",color="Category",title="Sales and Profit relationship")
st.plotly_chart(fig,use_container_width=True)


# fig =px.pie(filtered_df,names='Sub-Category',values='Profit',title="Order Count of Categories Sub-Catagory")
# st.plotly_chart(fig)