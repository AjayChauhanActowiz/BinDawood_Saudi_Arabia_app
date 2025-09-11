import requests
import json

url = "https://kbghg5mr5e-3.algolianet.com/1/indexes/spree_products/query?x-algolia-agent=Algolia%20for%20JavaScript%20(4.9.1)%3B%20Browser"

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

# Algolia expects the payload as a JSON string in the POST body
response = requests.post(url, headers=headers, data=json.dumps(payload))

# Print the response
print(response.status_code)
print('Almarai Fresh Milk Full Fat 2 L' in response.text)
