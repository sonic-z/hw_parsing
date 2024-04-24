import json
import time

import requests
from bs4 import BeautifulSoup
from fake_headers import Headers


def get_fakeheaders():
    return Headers(browser="chrome", os='win', headers=True).generate()


def main():
    response = requests.get('https://spb.hh.ru/search/vacancy?text=python&area=1&area=2',
                            headers=get_fakeheaders()).text

    main_page = BeautifulSoup(response, "lxml")

    vac_item = main_page.findAll('div', {'class': 'vacancy-serp-item-body'})
    vac_full_list = []

    for vac in vac_item:
        time.sleep(1)
        a_tag = vac.find('a', class_='bloko-link')
        link = a_tag['href']
        vac_response = requests.get(link, headers=get_fakeheaders()).text
        vac_page = BeautifulSoup(vac_response, "lxml")
        vac_info = vac_page.find('div', {'data-qa': 'vacancy-description'}).text.strip()
        if vac_info.upper().find('DJANGO') > 0 or vac_info.upper().find('FLASK') > 0:
            try:
                salary = vac.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).text.strip()
            except:
                salary = ''
            city = vac.find('div', {'data-qa': 'vacancy-serp__vacancy-address'}).text.strip()
            company_name = vac.find('div', class_='vacancy-serp-item__meta-info-company').text.strip()
            vac_full_list.append({
                'link': link,
                'name': a_tag.text.strip(),
                'salary': salary,
                'company_name': company_name,
                'city': city
            })
            print(link)

    with open('result.json', 'w', encoding='utf-8') as f:
        json.dump(vac_full_list, f, ensure_ascii=False, indent=4)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
