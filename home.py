import streamlit as st
import pandas as pd
import sqlite3

st.title('DASHBOARD')
st.subheader('Datasets Metadata')

# Load data
conn = sqlite3.connect('DATA/intelligence_platform.db')
df = pd.read_sql("SELECT * FROM datasets_metadata", conn)
conn.close()


col1, col2 = st.columns(2)

with col1:
    st.write("Dataset (Rows)")
    chart_data1 = df.set_index('columns')['rows']
    st.line_chart(chart_data1)


with col2:
    st.write(" Dataset (Columns)")
    chart_data2 = df.set_index('name')['columns']
    st.bar_chart(chart_data2)

st.subheader("Datasets Metadata Table")
st.dataframe(df)








