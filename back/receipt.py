import io
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env.local")
endpoint = os.environ.get("DI_ENDPOINT")
key = os.environ.get("DI_KEY")

def detect_data(f):
    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )
    bytes_io = io.BytesIO(f)
    f = io.BufferedReader(bytes_io)
    poller = document_analysis_client.begin_analyze_document(
        "prebuilt-receipt", document=f, locale="en-US")
    
    receipts = poller.result()

    items = []
    for _, receipt in enumerate(receipts.documents):
        if receipt.fields.get("Items"):
            for _, item in enumerate(receipt.fields.get("Items").value):
                item_description = item.value.get("Description")
                description = ""
                if item_description:
                   description = item_description.value
                   
                item_quantity = item.value.get("Quantity")
                quantity = 0
                if item_quantity:
                    quantity = item_quantity.value
                    
                item_total_price = item.value.get("TotalPrice")
                price = 0
                if item_total_price:
                    price = item_total_price.value
                    
                if description != "" and len(description) >= 5:
                    items.append({"name": description, "quantity": quantity, "price": price})
    return items