from curl_cffi import requests
# import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import json
import random
import string

def generate_random_string(length=16):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

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
# import urllib3
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# token = "token"
# proxyModeUrl = "http://{}:@proxy.scrape.do:8080".format(token)
# proxies = {
#     "http": proxyModeUrl,
#     "https": proxyModeUrl,
# }
def response_check(start_iteration, num_requests):
    """Perform multiple requests inside one thread to reduce overhead."""
    batch_results = []
    for i in range(num_requests):
        iteration = start_iteration + i
        st = time.time()
        try:
            response = requests.get(
                'https://www.bindawood.sa/en/api/master_products/15342',
                # params=params,
                # headers=headers,
                headers=genetrate_header(),
                # data=json.dumps(payload)
                # cookies=cookies,
                # impersonate='chrome120',
                # proxies=proxies,
                # verify=False
            )
            if fr'Almarai Fresh Milk Full Fat 2 L' in response.text:
                batch_results.append({
                    'iteration': iteration,
                    'status': response.status_code,
                    'response': 'good',
                    'time_taken': time.time()-st
                })
            else:
                batch_results.append({
                    'iteration': iteration,
                    'status': response.status_code,
                    'response': 'bad',
                    'time_taken': time.time() - st
                })
        except Exception as e:
            batch_results.append({
                'iteration': iteration,
                'status': None,
                'response': f'error: {e}',
                'time_taken': time.time() - st
            })
    return batch_results

results = []
thread_count = 20
total_requests = 3000
requests_per_thread = 10  # Each worker handles 10 requests

with ThreadPoolExecutor(max_workers=thread_count) as executor:
    futures = []
    for start in range(1, total_requests + 1, requests_per_thread):
        futures.append(executor.submit(response_check, start, requests_per_thread))

    for future in as_completed(futures):
        batch = future.result()
        for result in batch:
            print(result)
            results.append(result)

# Save results to Excel
file_name = 'BinDawood_app_pdp_feasibility_test'
df = pd.DataFrame(results)
df.to_excel(f'{file_name}.xlsx', index=False)
print(f"Results saved to {file_name}.xlsx")



