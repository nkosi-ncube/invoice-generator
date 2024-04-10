import streamlit as st
from InvoiceGenerator.api import Invoice, Item, Client, Provider, Creator
from InvoiceGenerator.pdf import SimpleInvoice
from datetime import datetime
import os
# Initialize invoice


os.environ["INVOICE_LANG"] = "en"
invoice = Invoice(Client('Client company'), Provider('My company'), Creator('John Doe'))
invoice.currency_locale = 'en_US.UTF-8'
invoice.currency = "R"
invoice.number = 10
invoice.name = 'stamp name'

# Get user input for invoice items
st.title("Invoice Generator")
num_items = st.number_input("Enter the number of invoice items", min_value=1, max_value=10, key="num_items")

item_descriptions = []
item_rates = []
item_taxes = []

for i in range(num_items):
    description = st.text_input(f"Enter item description {i+1}", key=f"description_{i}")
    item_descriptions.append(description)

    rate = st.number_input(f"Enter item rate {i+1}", min_value=0.01, key=f"rate_{i}")
    item_rates.append(rate)

    tax = st.selectbox(f"Select item tax {i+1}", [0, 15, 21], key=f"tax_{i}")
    item_taxes.append(tax)

# Create invoice items
for i in range(num_items):
    invoice.add_item(Item(item_rates[i], item_rates[i] * 100, description=item_descriptions[i], tax=item_taxes[i]))

# Get user input for provider and creator
st.title("Provider and Creator Details")
provider_name = st.text_input("Enter Provider Name:", key="provider_name")
provider_bank_account = st.text_input("Enter Provider Bank Account:", key="provider_bank_account")
provider_bank_code = st.text_input("Enter Provider Bank Code:", key="provider_bank_code")
provider_bank_name = st.text_input("Enter Provider Bank Name:", key="provider_bank_name")
provider_vat_id = st.text_input("Enter Provider VAT ID:", key="provider_vat_id")
provider_logo_filename = st.text_input("Enter Provider Logo Filename:", key="provider_logo_filename")
provider_vat_note = st.text_input("Enter Provider VAT Note:", key="provider_vat_note")
provider_email = st.text_input("Enter Provider Email:", key="provider_email")

creator_name = st.text_input("Enter Creator Name:", key="creator_name")

if st.button("Generate Invoice"):
    provider = Provider(provider_name, bank_account=provider_bank_account, bank_code=provider_bank_code, bank_name=provider_bank_name,
                        vat_id=provider_vat_id, logo_filename=provider_logo_filename,
                        vat_note=provider_vat_note,
                        email=provider_email,
                       )
    creator = Creator(creator_name)

    invoice.provider = provider
    invoice.creator = creator

    # Generate invoice
    invoice.stamp_filename = "stamp.png"
    invoice.date = datetime.now()
    invoice.paytype = "EFT"
    invoice.title = "Airconditioning Services"
    pdf = SimpleInvoice(invoice)
    pdf.gen("invoice.pdf", generate_qr_code=True)

    # Display generated invoice
    st.download_button("Download Invoice", data=open("invoice.pdf", "rb").read(), file_name="invoice.pdf")
