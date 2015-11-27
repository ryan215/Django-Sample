import requests
from django.conf import settings
import json
from django.contrib.auth import get_user_model

"""
This module assumes you are using a Custom User type model inherited from AbstractUserModel
These are shopify functions that will be inserted into the Custom user model
"""
shop_url = settings.SHOPIFY_STORE


def requests_search(email):
    # search their customer data base by email
    global shop_url

    request = requests.Session()
    request.auth = (settings.SHOPIFY_API_KEY, settings.SHOPIFY_API_PASSWORD)
    local_url = shop_url + "/customers/search.json"
    response = request.get(local_url + "?query=" + email)
    response_json = response.json()

    if 'customers' in response_json:
        customers = response_json['customers']
        for customer in customers:
            if customer['email'] == email:
                return customer
    #if it finishes then it doesn't exists so raise
    return None


def customer_create(self, password): # shopify_create
    global shop_url
    create_url = shop_url + "/customers.json"
    request = requests.Session()
    request.auth = (settings.SHOPIFY_API_KEY, settings.SHOPIFY_API_PASSWORD)

    try:
        metafield_value = self.referred_by.get_shopify_id()
    except:
        #change this default value to Rories shopify value
        metafield_value = 182863329
    address = self.get_address()
    address['country'] = 'US'
    new_customer = {
        "customer": {"first_name": self.first_name,
                     "last_name": self.last_name,
                     "email": self.email,
                     "verified_email": True,
                     "password": password,
                     "password_confirmation": password,
                     "tags": str(metafield_value),
                     "addresses": [address]
        }
    }

    new_customer = json.dumps(new_customer)

    customer = requests_search(self.email)

    if not customer:
        # create a new customer if one doesn't exists
        response = request.post(create_url, data=new_customer, headers={'Content-Type': 'application/json'})
        response_json = response.json()
        if 'errors' in response_json:
            return response_json
        customer = response_json['customer']
    self.shopify_id = customer['id']
    self.save()


def customer_get(self): # shopify_get
    global shop_url
    request = requests.Session()
    request.auth = (settings.SHOPIFY_API_KEY, settings.SHOPIFY_API_PASSWORD)
    local_url = shop_url + "/customers/" + str(self.shopify_id) + ".json"
    response = request.get(local_url)
    response_json = response.json()
    if 'errors' in response_json:
        return response_json
    return response_json


def customer_metafield(self): # shopify_metafield
    global shop_url
    request = requests.Session()
    request.auth = (settings.SHOPIFY_API_KEY, settings.SHOPIFY_API_PASSWORD)
    local_url = shop_url + "/customers/" + str(self.shopify_id) + "/metafields.json"
    response = request.get(local_url)
    response_json = response.json()
    if 'errors' in response_json:
        return response_json

    for meta in response_json['metafields']:
        print meta['key']
        print meta['value']


def customer_delete(self): # shopify_delete
    global shop_url
    request = requests.Session()
    request.auth = (settings.SHOPIFY_API_KEY, settings.SHOPIFY_API_PASSWORD)
    local_url = shop_url + "/customers/" + str(self.shopify_id) + ".json"
    response = request.delete(local_url)
    response_json = response.json()
    if 'errors' in response_json:
        return response_json
    return True


def customer_edit(self):
    """
    this function goes and edits shopify
    """
    address = self.get_address()
    address['country'] = 'US'
    edit_customer_json = {
    "customer": {"first_name": self.first_name,
                 "last_name": self.last_name,
                 "email": self.email,
                 "verified_email": True,
                 "addresses": [address],
    }
    }
    edit_customer_json = json.dumps(edit_customer_json)

    request = requests.Session()
    request.auth = (settings.SHOPIFY_API_KEY, settings.SHOPIFY_API_PASSWORD)
    local_url = shop_url + "/customers/" + str(self.shopify_id) + ".json"
    response = request.put(local_url, data=edit_customer_json, headers={'Content-Type': 'application/json'})
    response_json = response.json()
    if 'errors' in response_json:
        return response_json
    return response_json


def customer_orders(self): # shopify_orders
    request = requests.Session()
    request.auth = (settings.SHOPIFY_API_KEY, settings.SHOPIFY_API_PASSWORD)
    local_url = shop_url + "/orders.json?customer_id=" + str(self.shopify_id) + ".json"
    response = request.get(local_url)
    response_json = response.json()
    if 'errors' in response_json:
        return response_json
    return response_json


def customer_sales_to_date(self): # shopify_sales
    from user_app.models import CustomUser
    """
    using shopify_id will search shopify tags
    pertaining to that id to find a list of customers
    """
    global shop_url
    request = requests.Session()
    request.auth = (str(settings.SHOPIFY_API_KEY), str(settings.SHOPIFY_API_PASSWORD))
    if self.shopify_id == 0:
        return {'errors':'no shopify id'}
    local_url = shop_url + "/customers/search.json?query=" + str(
        self.shopify_id) + "&limit=250&fields=total_spent,email"
    response = request.get(local_url)
    response_json = response.json()

    if 'customers' in response_json:
        customers = response_json['customers']
        total_earned = 0
        total_customers = len(customers)
        users = []
        for customer in customers:
            total_earned += float(customer['total_spent'])
            try:
                user = CustomUser.objects.get(email=customer['email']).get_all_data()
                user['total_spent'] = "$" + (customer['total_spent'])
                users.append(user)
            except:
                continue

    return_json = {
        'users': users,
        'total_customers': total_customers,
        'total_earned': "${0:.2f}".format(total_earned),
    }
    if 'errors' in response_json:
        return response_json
    return return_json


def count_customers():
    global shop_url
    request = requests.Session()
    request.auth = (settings.SHOPIFY_API_KEY, settings.SHOPIFY_API_PASSWORD)
    local_url = shop_url + "/customers/count.json"
    response = request.get(local_url)
    response_json = response.json()
    if 'errors' in response_json:
        return response_json
    return response_json['count']


def test_function():
    global shop_url
    request = requests.Session()
    request.auth = (settings.SHOPIFY_API_KEY, settings.SHOPIFY_API_PASSWORD)
    local_url = shop_url + "/customers/182863329.json"
    response = request.get(local_url)
    response_json = response.json()
    if 'errors' in response_json:
        return response_json
    return response_json['customer']


def update_local_host():
    from user_app.models import CustomUser

    lef_users = CustomUser.objects.all()
    for user in lef_users:

        customer = requests_search(user.email)
        if not customer:
            # create a new customer if one doesn't exists
            # response = request.post(create_url, data=new_customer, headers={'Content-Type': 'application/json'})
            #response_json  = response.json()
            print 'doesnt exists'
            continue
        user.shopify_id = customer['id']

        user.save()
        #self.save()