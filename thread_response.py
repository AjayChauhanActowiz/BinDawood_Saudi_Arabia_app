from curl_cffi import requests
# import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import json


headers = {
    "Accept-Encoding": "gzip",
    "Connection": "Keep-Alive",
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "okhttp/4.11.0",
    "x-algolia-api-key": "621d5582caa0a68f0fdf372bcae9ab86",
    "x-algolia-application-id": "KBGHG5MR5E"
}

payload = {
    "query": "milk",
    "clickAnalytics": True,
    "hitsPerPage": 10,
    "facetFilters": [
        ["taxons_en.lvl1:Departments > Dairy & Eggs"]
    ],
    "numericFilters": ["price>=0"],
    "enablePersonalization": False,
    # "userToken": "anonymous-7cf2875e-2ed8-4aeb-8561-2da715d6c53b",
    "filters": "tenant_id = 2 AND (availability_type: regular OR availability_type: \"regular_and_express\")",
    "attributesToRetrieve": [
        "master_id",
        "weighted",
        "image",
        "price",
        "name_ar",
        "full_name_ar",
        "name_en",
        "full_name_en",
        "in_stock",
        "express",
        "weight_increment",
        "max_weight_per_order",
        "min_weight_per_order",
        "inventory_modifiers",
        "taxons_ar",
        "taxons_en",
        "preferred_cuts",
        "validity_tag_ar",
        "validity_tag_en",
        "loyalty_point",
        "marketing_tag_details",
        "moq_limit",
        "weight",
        "perform_liquid_weight_check",
        "variants",
        "has_campaign_per_person_limit",
        "tenant_id",
        "availability_type",
        "depend_only_inventory_details",
        "brand_en",
        "brand_ar",
        "image",
        "price",
        "calories",
        "tenant_id",
        "subscription_only"
    ]
}
# import urllib3
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# token = "f42a5b59aec3467e97a8794c611c436b91589634343"
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
            response = requests.post(
                'https://kbghg5mr5e-3.algolianet.com/1/indexes/spree_products/query?x-algolia-agent=Algolia%20for%20JavaScript%20(4.9.1)%3B%20Browser',
                # params=params,
                headers=headers,
                data=json.dumps(payload)
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
file_name = 'BinDawood_app_pl_feasibility_test'
df = pd.DataFrame(results)
df.to_excel(f'{file_name}.xlsx', index=False)
print(f"Results saved to {file_name}.xlsx")


