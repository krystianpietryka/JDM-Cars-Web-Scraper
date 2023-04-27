import requests
from bs4 import BeautifulSoup

url = 'https://www.beforward.jp/stocklist/icon_clearance=1/sortkey=q'
homepage_url = 'beforward.jp'

page = requests.get(url)

soup = BeautifulSoup(page.content, "html.parser")

all_offers = soup.find("div", class_="cars-box-stocklist-renewal")

# with open("offers.txt", 'w', encoding='utf-8') as o:
#     for line in str(all_offers.prettify()):
#         o.write(line)

car_offers = all_offers.find_all("tr", class_="stocklist-row")


for car_offer in car_offers:
    try:
    # file_name = ("car_offer" + str(name_int))
    # with open(file_name, 'w', encoding='utf-8') as file:
    #     for line in str(car_offer):
    #         file.write(line)
    # name_int += 1

        make_model_p= car_offer.find("p", class_="make-model")
        make_model_a = make_model_p.find("a",{"class":"vehicle-url-link"})
        make_model = make_model_a.contents[0].strip()
        vehicle_url = str(homepage_url) + str(make_model_a.get("href"))
        car_model = make_model_a.contents[0].strip()

        mileage_td = car_offer.find("td", class_ = "basic-spec-col basic-spec-col-bordered mileage")
        mileage = mileage_td.find("p", class_='val').contents[0].strip()
        year_td = car_offer.find("td", class_ = "basic-spec-col basic-spec-col-bordered year")
        year = year_td.find("p", class_='val').contents[0].strip()
        engine_td = car_offer.find("td", class_ = "basic-spec-col basic-spec-col-bordered engine")
        engine = engine_td.find("p", class_='val').contents[0].strip()
        location_td = car_offer.find("p", class_ = "val stock-area")
        location = location_td.find("span").contents[0].strip()
        
        print('\n\n')
        print(vehicle_url)
        print(car_model)
        print(mileage)
        print(year)
        print(engine)
        print(location)
    except Exception as e:
        print(e)
        pass

# with open("offers.txt", 'w', encoding='utf-8') as o:
#     o.write(str(car_offers[0]))