import streamlit as st
import pandas as pd
import base64
from io import BytesIO


def get_table_download_link(df, filename):

    """Generates a link allowing the data in a given panda dataframe to be downloaded"""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Sheet1', index=False)
    output.seek(0)
    b64 = base64.b64encode(output.read()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">Download Excel File</a>'
    return href



def find_duplicates(data):
    """Identify duplicate payments in the provided dataframe"""
    return data[data.duplicated(subset=['WRBTR', 'XBLNR', 'BLDAT'], keep=False)].sort_values(
        by='Document Number', ascending=True)



# Streamlit app title
st.title('Duplicate Payments Finder')

# Upload section
uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")

if uploaded_file is not None:
    data = pd.read_excel(uploaded_file)

    # Display section
    st.write("Uploaded Data Overview:")
    st.write(data.head())

    # Duplicate identification section
    st.subheader('Duplicate Payments')
    duplicates = find_duplicates(data)

    if not duplicates.empty:
        st.write(duplicates)

        # Download section
        st.markdown(get_table_download_link(duplicates, 'duplicates.xlsx'), unsafe_allow_html=True)
    else:
        st.write("No duplicate payments found!")

else:
    st.write("Please upload an Excel file to identify duplicate payments.")

