import requests
from bs4 import BeautifulSoup

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0'}
list_base = []
count = 0

def gener_catalog():
    catalogs_list = []
    response = requests.get("https://www.strategshop.ru/", headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.find_all('li', class_="open")
    for item in items:
        catalog = str(item.find('a')['href'])
        if catalog.count("/") == 3:
            catalogs_list.append(catalog)
    return catalogs_list

def Adding_databases(text):
    a = (text.replace('"', '').replace("'", "").replace("{", "").replace("}", ""))
    link_product = "https://www.strategshop.ru/" + a[a.find("href=") + 6:]
    list_base.append(["Название: {}".format(a[a.find("name:") + 5: a.find("id") - 1]),
                      "Бренд: {}".format(a[a.find("brand:") + 6: a.find("position") - 1]),
                      "Цена: {}".format(a[a.find("price:") + 6: a.find("category") - 1]),
                      "Код товара: {}".format(int(a[a.find("id:") + 3: a.find("price") - 1])),
                      "Максимальное кол-чи: {}".format(Adding_database_plus("Data_max", link_product)),
                      "Сылка на товар: " + link_product])
    print(a[a.find("name:") + 5: a.find("id") - 1], count)

def Adding_database_plus(Mode_for, link):
    response = requests.get(link, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")
    try:
        if Mode_for == "Data_max":
            items = str(soup.find("div", class_="q-container q-container-").get_text)
            return int(items[items.find("только") + 7: items.find("только") + 9])
    except AttributeError:
        return 0

for catalog in gener_catalog():
    print(catalog)
    page = 1
    while True:
        if page == 1:
            response = requests.get("https://www.strategshop.ru{}".format(catalog), headers=HEADERS)
        else:
            response = requests.get("https://www.strategshop.ru{}page{}/".format(catalog, page), headers=HEADERS)
        soup = BeautifulSoup(response.content, 'html.parser')
        items = soup.find_all('h3', class_="raw")
        if (len(items)):
            for item in items:
                text_base = str(item.find('a').get_text).replace("<", "").replace("}", "").replace("]", "}")[
                    str(item.find('a').get_text).find("products") + 8: str(item.find('a').get_text).find("onclick") - 8]
                count += 1
                Adding_databases(text_base)
            page += 1
            print("Cтраница обработана {}: Всего елементов: {}".format((page - 1), count))
        else:
            break

file = open("base_strategshop.txt", "w")
for row in list_base:
    file.write(' '.join([str(elem) for elem in row]))
    file.write('\n')