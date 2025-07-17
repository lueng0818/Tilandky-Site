## utils/mailchimp.py
```python
import os
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

API_KEY = os.getenv("MAILCHIMP_API_KEY")
SERVER = os.getenv("MAILCHIMP_SERVER_PREFIX")
LIST_ID = os.getenv("MAILCHIMP_LIST_ID")

client = Client()
client.set_config({
    "api_key": API_KEY,
    "server": SERVER
})

def subscribe_email(email: str) -> bool:
    try:
        client.lists.add_list_member(LIST_ID, {"email_address": email, "status": "subscribed"})
        return True
    except ApiClientError as error:
        print(error.text)
        return False
