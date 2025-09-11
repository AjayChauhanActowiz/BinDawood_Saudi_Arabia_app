import requests
import random
import string
def generate_random_string(length=16):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
url = "https://www.bindawood.sa/en/api/master_products/15342"
def genetrate_header():
    headers = {
        "accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip",
        "Connection": "Keep-Alive",
        "User-Agent": "okhttp/4.11.0",
        # "x-device-id": "542b5bb6ec7705ac",
        "x-device-id": generate_random_string(),
        "x-spree-platform": "android",
        "x-spree-supermarketid": "2",
        "x-view-version": "2"
    }
    return headers

response = requests.get(url, headers=genetrate_header())

# Print status code and JSON response
print(response.status_code)
print(response.text)
