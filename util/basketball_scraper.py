import requests
import urllib.request
from bs4 import BeautifulSoup

def scrape_all_players_contracts(url):
    #given the url of all contracts, return dict of [name] -> (current year salary, next, so on)
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    salaries = {}
    
    rows = soup.find_all("tr")
    for row in rows:
        
        all_salary = row.find_all(attrs={"data-stat": True})
        if all_salary == [] or not all_salary[0].text.isnumeric():
            continue
        name = all_salary[1].text
        salaries[name] = [element.text for element in all_salary[3:-3] if element.text != ""]

    meta = [a.text for a in rows[1].find_all(attrs={"data-stat": True})[3:-3]]
    salaries["METADATA"] = meta
    return salaries

    
