import streamlit as st
import pandas as pd
import base64

def download_link(object_to_download, download_filename, download_link_text):

    if isinstance(object_to_download,pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=False)
        b64 = base64.b64encode(object_to_download.encode()).decode()
        return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'

def main():

    item = st.sidebar.radio("Filters", ('Select All','Fruit','Vegetable'))
    data = pd.read_excel("BQ-Assignment-Data-Analytics.xlsx")

    if item == 'Select All':
        st.write(data)

    if item == 'Fruit':
        data = data[data['Item Type']=='Fruit']
        st.write(data)

    if item == 'Vegetable':
        data = data[data['Item Type']=='Vegetable']
        st.write(data)

    if st.button('Download'):
        tmp_download_link = download_link(data, 'YOUR_DF.csv', 'Click here to download your data!')
        st.markdown(tmp_download_link, unsafe_allow_html=True)

st.title("Internship Assignment")
st.sidebar.title("Filter")

if __name__ == "__main__":
    main()
