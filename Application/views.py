from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import re
from Application.models import MerchantInfo, Product, ProductSeller
from django.http import JsonResponse


# Create your views here.


def save_product(request):
    def get_data(url):
        glassdor = requests.get(url)
        data = {}

        if glassdor.status_code == 200:
            soup = BeautifulSoup(glassdor.content, 'html.parser')
            data['name'] = soup.find('h1').text
            data['price'] = soup.find('div', {'class': 'product-price-container'}).text.replace('Sepet Fiyatı', '')
            data['brand'] = soup.find('h1', {'class': 'pr-new-br'}).a.text
            data['category'] = soup.find('div', {'class': 'product-detail-breadcrumb full-width'}).findAll('span')[
                -1].text
            data['merchant_name'] = soup.find('div', {'class': 'merchant-box-wrapper'}).find('a').text
            merchant_profile_url = soup.find('div', {'class': 'merchant-box-wrapper'}).find('a').attrs['href']
            merchant_profile_url = merchant_profile_url.split('?')[0]
            merchant_profile_url = f"/magaza/profil{merchant_profile_url.split('magaza')[1]}"
            merchant_profile_link = f"https://www.trendyol.com{merchant_profile_url}"
            mercant_glassdor = requests.get(merchant_profile_link)
            mercant_soup = BeautifulSoup(mercant_glassdor.content, 'html.parser')
            print(mercant_soup.findAll('span', {'class': 'seller-info-container__wrapper__text-container__value'}))
            data['mercant_city'] = \
                mercant_soup.findAll('span', {'class': 'seller-info-container__wrapper__text-container__value'})[
                    1].text
            data['merchant_score'] = soup.find('div', {'class': 'sl-pn'}).text
            other_merchants_obj = soup.findAll('div', {'class': 'pr-mc-w gnr-cnt-br'})
            other_merchants = []
            for other_merchant in other_merchants_obj:
                other_merchants.append({'name': other_merchant.div.div.div.div.a.text,
                                        'score': other_merchant.div.div.div.select('.sl-pn')[0].text,
                                        'product_price': other_merchant.select('.prc-dsc')[0].text})

            data['other_merchants'] = other_merchants
            return data
        else:
            print('Error Status Code:', glassdor.status_code)

    url = request.GET.get("url")
    product_data = get_data(url)
    merchant = MerchantInfo.objects.create(name=product_data['merchant_name'], city_name=product_data['mercant_city'],
                                           seller_score=product_data['merchant_score'])
    product = Product.objects.create(name=product_data['name'], brand=product_data['brand'],
                                     category=product_data['category'])
    ProductSeller.objects.create(merchant=merchant, product=product, selling_price=product_data['price'],
                                 discounted_price=product_data['price'])

    for other_merchant in product_data['other_merchants']:
        other_merchant_obj = MerchantInfo.objects.create(name=other_merchant['name'],
                                                         seller_score=other_merchant['score'])
        ProductSeller.objects.create(merchant=other_merchant_obj, product=product,
                                     selling_price=other_merchant['product_price'],
                                     discounted_price=other_merchant['product_price'])

    return JsonResponse({'status': True})
