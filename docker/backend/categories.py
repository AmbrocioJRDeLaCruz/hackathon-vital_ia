from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os
import ast

load_dotenv(dotenv_path=".env.local")

llm = AzureChatOpenAI(
    openai_api_key = os.environ.get("AZURE_OPENAI_API_KEY"),
    azure_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT"),
    api_version = os.environ.get("AZURE_API_VERSION"),
    azure_deployment = os.environ.get("AZURE_DEPLOYMENT")
)

def identify(items):

    items_to_send = [item['name'] for item in items]
    system_message="""You have been assigned the following task: 

    1. Given a list, identify the product for each entry. The product name is found within the text of name field. 
    2. After identifying the product name, determine the associated category for this product. 
    3. If the identified product is a mixture of products, associate the most appropriate category, if no specific category exists, indicate as "Processed".

    For example, given the list:

            ["MCV MILK CHOC DIGS, "HOVIS S CHEESE 7S 800G"]

    We can indicate that for the first element the product is "Milk" and its category is "Dairy". While, for the second element the product is "Cheese" and its category is "Dairy"

    You should send back a object with schema similar to:  [{'x': 'product', 'y': 'category'},{'x': 'product', 'y': 'category'}]
    
    Send only the json code withouth tags ```json or ```.
    """

    response = llm.invoke([SystemMessage(content=system_message)]+[HumanMessage(content=str(items_to_send))])
    data = ast.literal_eval(response.content)
    for i, item in enumerate(items):
        item['name'] = data[i]['x']
        item['category'] = data[i]['y']
    return items
