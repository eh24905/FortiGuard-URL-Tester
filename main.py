import requests
import re
from bs4 import BeautifulSoup
from colorama import Fore, Back, Style

page = requests.get('http://www.fortiguard.com/webfilter/categories')

soup = BeautifulSoup(page.content, 'html.parser')

tables = soup.find('section', class_="ency_content").find_all('table')

for x in tables[0:-1]:
    major_category = x.find_previous_sibling('h2').text

    http_links = x.find_all('a', href=re.compile(r'http://'))

    print(Style.BRIGHT + major_category + Style.RESET_ALL)

    for a in http_links:
        href = a["href"]
        category = str(soup.find(href=href).find_parent(
            'td').find_previous_sibling('td').find_previous_sibling('td').text)

        try:
            r = requests.get(href)
            if "<h1>FortiGuard Web Filtering Test Page</h1>" in r.text:
                print(category + " - " + Fore.GREEN +
                      'Allowed' + Style.RESET_ALL)
            else:
                print(category + ' - ' + Fore.RED +
                      'Blocked' + Style.RESET_ALL)
        except Exception as e:
            raise e

    print('\n')
