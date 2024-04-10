import os

from tempfile import NamedTemporaryFile

from InvoiceGenerator.api import Invoice, Item, Client, Provider, Creator
from InvoiceGenerator.pdf import SimpleInvoice
from datetime import datetime

# choose english as language
os.environ["INVOICE_LANG"] = "en"

client = Client('Client company')
provider = Provider('My company', bank_account='2600420569',bank_code="470010",bank_name="Capitec",
vat_id=12,logo_filename="logo.jpeg",
vat_note="this is your vat",
email="nkosi@codegarden.co.za",
)
creator = Creator('John Doe')

invoice = Invoice(client, provider, creator)
invoice.currency_locale = 'en_US.UTF-8'
invoice.currency="R"
invoice.number =10
invoice.name ='stamp name'
invoice.add_item(Item(32, 600, description="Item 1"))
invoice.add_item(Item(60, 50, description="Item 2", tax=21))
invoice.add_item(Item(50, 60, description="Item 3", tax=0))
invoice.add_item(Item(5, 600, description="Item 4", tax=15))
invoice.stamp_filename ="stamp.png"
invoice.date = datetime.now()
invoice.paytype = "EFT"
invoice.title="Airconditioning Services"
pdf = SimpleInvoice(invoice)
pdf.gen("invoice.pdf", generate_qr_code=True)