#Imports
import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Set up our App
st.set_page_config(page_title="💿 Data Sweeper",layout="wide")

#Custom Css
st.markdown(
    """
    <style>
    .stApp{
       background-color:black;
       color:white;
    }
    </style>
    """,
    unsafe_allow_html= True
)

#Title and Description
st.title("💿 Datasweeper Sterling Integrator By Taha Hussain")
st.write("Transform your files between csv and Exel formats with built-in data cleaning and visualization creating the project for quater 3!")

#file uploader

uploaded_file = st.file_uploader("Upload your files (accepts CSV or Exel):",type=["cvs","xlsx"],accept_multiple_files=(True))

if uploaded_file:
    for file in uploaded_file:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == "xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"unsupported file type: {file_ext}")
            continue

        #file details
        st.write("🔎 Preview the head of the Dataframe")
        st.dataframe(df.head())

      #data cleaning options

st.subheader("⚒ Data Cleaning Options")
if st.checkbox(f"Cleaning data for{file.name}"):
    col1,col2 = st.columns(2)
    
    with col1:
        if st.button(f"Remove duplicates from the file : {file.name}"):
            df.drop_duplicates(inplace=True)
            st.write("🔴 Duplicates Remove!")

    with col2:
        if st.button(f"Fill missing values for {file.name}"):
            numeric_cols = df.select_dtypes(includes=['number']).columns
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
            st.write('🚦 Missing values have been filled!')

st.subheader("✅ Select Colums to keep")   
columns = st.multiselect(f"choose columns for {file.name},",df.columns,default=df.columns)
df = df[columns]

#Data Visualization
st.subheader("📊 Data Visualization")
if st.checkbox(f"Show Visualization for {file.name}"):
    st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

    #Conversion Options

    st.subheader("🔄 Conversion Options")
    conversion_type = st.radio(f"Convert {file.name} to:", ["CVS", "Excel"], key=file.name)
    if st.button(f"convert{file.name}"):
        buffer = BytesIO()
        if conversion_type == "CVS":
            df.to_csv(buffer, index=False)
            file_name = file.name.replace(file_ext, ".CSV")
            mime_type = "text/csv"

        elif conversion_type == "Exel":
            df.to_excel(buffer, index=False)
            file_name = file.name.replace(file_ext, "xlsx")
            mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        buffer.seek(0)

        st.download_button(
            label=f"Download  {file.name} as {conversion_type}",
            data=buffer,
            file_name=file_name,
            mime=mime_type
        )
st.success("✅🚀 All files processed successfully!")

