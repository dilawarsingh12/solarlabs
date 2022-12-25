from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import CountryInfoSerializer
from bs4 import BeautifulSoup
import requests
import json
import string

@api_view(['GET'])
def get_data(request,country):
    url = 'https://en.wikipedia.org/wiki/'+country
    print(url)
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    infobox = soup.find("table", class_="infobox")

    flag_link = infobox.find("img")["src"]
    

    capital = [cap.text.strip() for cap in infobox.find("th", text="Capital").find_next("td").find_all("li")]

    if not capital:
        capital = infobox.find("th", text="Capital").find_next("td").find("a")

    for city in capital:
        if city[0] not in list(string.ascii_uppercase):            
            capital  = infobox.find("th", text="Capital").find_next("td").find("a")

    

    largest_city = infobox.find("tr", class_="mergedbottomrow").find("td").find("a").text.strip()

    

    total_text_element = infobox.find_all("th", text="• Total")

    area_total = total_text_element[0].find_next("td").text.strip()

    population_element = infobox.find("th", text="Population")
    population_val = population_element.find_next("td").text.strip()

    GDP_nominal = total_text_element[2].find_next("td").text.strip()

    official_languages_element = infobox.find(
        "tr", class_='mergedtoprow').find_next('td')

    official_languages = [
        language.text.strip()
        for language in official_languages_element.find_all("a")
    ]

    
    sep = '['    
    
    area = area_total.split(sep, 1)[0]    
    Area = area[:10]
    population = population_val.split(sep, 1)[0]
    GDP = GDP_nominal.split(sep, 1)[0]


    capitals = []
    print(capital)
    # Largest_Cities = []
    lang = []

    for i in official_languages:
       temp = i.split(sep, 1)[0].strip() 
       if temp and temp[0] in list(string.ascii_uppercase):
        lang.append(temp)

    for i in capital:
       temp = i.split(sep, 1)[0].strip() 
       if temp:
        capitals.append(temp)

        

      

    # for i in largest_city:
    #    temp = i.split(sep, 1)[0].strip()
    #    if len(temp)>0:
    #     Largest_Cities.append(temp)   
       

    val = {
            "flag_link": "https:"+flag_link,
            "capital": capitals,
            "largest_city": largest_city,
            "official_languages": lang,
            "area_total": Area,
            "population": population,
            "GDP_nominal": GDP
        }
    
    serializer = CountryInfoSerializer(data=val)
    serializer.is_valid(raise_exception=True)
    return Response(serializer.data)

       