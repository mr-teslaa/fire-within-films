import requests

def getLocation(ip_address):
    url = 'https://get.geojs.io/v1/ip/geo/'+ip_address+'.json'

    geo_request = requests.get(url)
    geo_data = geo_request.json()

    if 'region' and 'city' in geo_data:
        ip = geo_data['ip']
        country = geo_data['country']
        area_code = geo_data['area_code']
        city = geo_data['city']
        region = geo_data['region']
        isp_organization = geo_data['organization']
        isp_organization_name = geo_data['organization_name']
        asn = geo_data['asn']
        timezone = geo_data['timezone']
        accuracy = geo_data['accuracy']
        latitude = geo_data['latitude']
        longitude = geo_data['longitude']
        continent_code = geo_data['continent_code']

        return ip, country, area_code, city, region, isp_organization, isp_organization_name, asn,timezone, accuracy, latitude, longitude, continent_code
    else:
        ip = geo_data['ip']
        country = geo_data['country']
        area_code = geo_data['area_code']
        isp_organization = geo_data['organization']
        isp_organization_name = geo_data['organization_name']
        asn = geo_data['asn']
        timezone = geo_data['timezone']
        accuracy = geo_data['accuracy']
        latitude = geo_data['latitude']
        longitude = geo_data['longitude']
        continent_code = geo_data['continent_code']

        return ip, country, area_code, isp_organization, isp_organization_name, asn,timezone, accuracy, latitude, longitude, continent_code
