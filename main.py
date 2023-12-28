import pandas as pd
import streamlit as st
import base64
import pdfkit
import os
import tempfile
import matplotlib.pyplot as plt
# Function to calculate entry fee based on kata and kumite
def calculate_entry_fee(row):
    if row['kata'] == 'Yes' and row['kumite'] == 'Yes':
        return 1500
    elif row['kata'] == 'Yes' or row['kumite'] == 'Yes':
        return 1000
    else:
        return 0

# Streamlit app
def main():
    st.title("Championship Entry Fee Calculator")

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        # Calculate entry fee
        df['entry_fee'] = df.apply(lambda row: calculate_entry_fee(row), axis=1)
        total_entry = df['entry_fee'].sum()

        # Calculate amounts and counts for 'Kata Only', 'Kumite Only', and 'Both Kata and Kumite'
        entry_fee_for_kata_only = df[(df['kata'] == 'Yes') & (df['kumite'] == 'No')]['entry_fee'].sum()
        entry_fee_for_kumite_only = df[(df['kata'] == 'No') & (df['kumite'] == 'Yes')]['entry_fee'].sum()
        entry_fee_for_both = df[(df['kata'] == 'Yes') & (df['kumite'] == 'Yes')]['entry_fee'].sum()

        number_of_kata_only = len(df[(df['kata'] == 'Yes') & (df['kumite'] == 'No')])
        number_of_kumite_only = len(df[(df['kata'] == 'No') & (df['kumite'] == 'Yes')])
        number_of_both = len(df[(df['kata'] == 'Yes') & (df['kumite'] == 'Yes')])

        # Display the results
        st.subheader("Results")
        st.write(f"Total Entry Fee: {total_entry}")
        st.write(f"Entry Fee for Kata Only: {entry_fee_for_kata_only}, Number of Participants: {number_of_kata_only}")
        st.write(f"Entry Fee for Kumite Only: {entry_fee_for_kumite_only}, Number of Participants: {number_of_kumite_only}")
        st.write(f"Entry Fee for Both Kata and Kumite: {entry_fee_for_both}, Number of Participants: {number_of_both}")

        # Display the table invoice
        st.subheader("Invoice Table")
        invoice_table = pd.DataFrame({
            'Category': ['Total Kata Only Participants', 'Total Kumite Only Participants', 'Total Both Participants', 'Total Amount'],
            'Number of Participans': [number_of_kata_only, number_of_kumite_only, number_of_both, len(df)],
            'Amount':[entry_fee_for_kata_only,entry_fee_for_kumite_only,entry_fee_for_both,total_entry]
        })
        st.table(invoice_table)

        # Downloadable invoice as PDF
        st.subheader("Download Invoice as PDF")
        st.write("Download your invoice in PDF format.")
        st.markdown(get_pdf_download_link(invoice_table), unsafe_allow_html=True)


# Function to create a download link for the PDF file
def get_pdf_download_link(table):
    # Plot the DataFrame as a table
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.axis('tight')
    ax.axis('off')
    table_ax = ax.table(cellText=table.values, colLabels=table.columns, cellLoc='center', loc='center')

    # Save the plot as a PDF file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        plt.savefig(temp_pdf, format='pdf', bbox_inches='tight')

    # Encode the PDF content
    with open(temp_pdf.name, "rb") as pdf_file:
        pdf_data = pdf_file.read()
        b64 = base64.b64encode(pdf_data).decode()

    # Create a download link
    href = f'<a href="data:application/pdf;base64,{b64}" download="invoice_table.pdf">Download PDF</a>'

    # Remove temporary file
    os.remove(temp_pdf.name)

    return href

if __name__ == "__main__":
    main()
