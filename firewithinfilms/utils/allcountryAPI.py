import requests

def getCountryList():
    url = "https://restcountries.com/v3.1/all"
    country_request = requests.get(url)
    country_data = country_request.json()

    for country in country_data:
        country_data = country['name']
        country_name = country_data['common']
    
    return country_name

   