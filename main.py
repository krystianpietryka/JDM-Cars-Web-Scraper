import requests
from bs4 import BeautifulSoup
import pandas as pd

errors = []
homepage_url = 'beforward.jp'

current_url = 'https://www.beforward.jp/stocklist/icon_clearance=1/page=1/sortkey=q'


current_page = requests.get(current_url)
current_page_soup = BeautifulSoup(current_page.content, "html.parser")
all_offers = current_page_soup.find("div", class_="cars-box-stocklist-renewal")

car_offers = all_offers.find_all("tr", class_="stocklist-row")

# Initialize empty lists to be used in pandas dataframe
vehicle_url_list = []
car_model_list =[]
mileage_list =[]
year_list =[]
engine_list =[]
location_list =[]
original_price_list =[]
current_price_list =[]
discount_list =[]
total_price_list =[]
shipping_price_list =[]
model_code_list =[]
steering_list =[]
fuel_list =[]
seats_list =[]
engine_code_list =[]
color_list =[]
drive_list =[]
doors_list =[]
auction_grade_list =[]
        

for car_offer in car_offers:
    try:
        make_model_p= car_offer.find("p", class_="make-model")
        make_model_a = make_model_p.find("a",{"class":"vehicle-url-link"})
        vehicle_url = str(homepage_url) + str(make_model_a.get("href"))
        # indexing from 1 if the first word is a year
        car_model = make_model_a.contents[0].split()
        if car_model[0].isnumeric():
            car_model = ' '.join(car_model[1:])
        else:
            car_model = ' '.join(car_model)

        mileage_td = car_offer.find("td", class_ = "basic-spec-col basic-spec-col-bordered mileage")
        mileage = mileage_td.find("p", class_='val').contents[0].strip()
        year_td = car_offer.find("td", class_ = "basic-spec-col basic-spec-col-bordered year")
        year = year_td.find("p", class_='val').contents[0].strip()
        engine_td = car_offer.find("td", class_ = "basic-spec-col basic-spec-col-bordered engine")
        engine = engine_td.find("p", class_='val').contents[0].strip()
        location_td = car_offer.find("p", class_ = "val stock-area")
        location = location_td.find("span").contents[0].strip()
        original_price = car_offer.find("p", class_ = "original-vehicle-price").contents[0].strip().replace(',', '')
        current_price =  car_offer.find("span", class_ = "price").contents[0].strip().replace('$', '').replace(",", '')
        discount = car_offer.find("p", class_ = "save-rate").contents[0].strip()
        total_price_p = car_offer.find("p", class_ = "total-price")
        total_price = total_price_p.find("span", class_=None).contents[0].strip().replace('$', '').replace(",", '')
        shipping_price = int(total_price) - int(current_price)

        table_detailed_spec = car_offer.find("table", class_ = "table-detailed-spec")
        table_rows = table_detailed_spec.find_all("tr")
        first_row = table_rows[0]
        second_row = table_rows[1]
        third_row = table_rows[2]

        model_code = first_row.find("td", class_="td-1st").contents[0].strip()
        steering = first_row.find("td", class_="td-2nd").contents[0].strip()
        fuel = first_row.find("td", class_="td-3rd").contents[0].strip()
        seats = first_row.find("td", class_="td-4th").contents[0].strip()

        engine_code = second_row.find("td", class_="td-1st").contents[0].strip()
        color = second_row.find("td", class_="td-2nd").contents[0].strip()
        drive = second_row.find("td", class_="td-3rd").contents[0].strip()
        doors = second_row.find("td", class_="td-4th").contents[0].strip()

        auction_grade = third_row.find("td", class_="td-colspan").contents[0].strip()

        print('\n\nSaving to excel:')
        print(vehicle_url)
        print(car_model)
        print(mileage)
        print(year)
        print(engine)
        print(location)
        print(original_price)
        print(current_price)
        print(discount)
        print(total_price)
        print(shipping_price)
        print(model_code)
        print(steering)
        print(fuel)
        print(seats)
        print(engine_code)
        print(color)
        print(drive)
        print(doors)
        print(auction_grade)
        print("\n\n")

        vehicle_url_list.append(vehicle_url)
        car_model_list.append(car_model)
        mileage_list.append(mileage)
        year_list.append(year)
        engine_list.append(engine)
        location_list.append(location)
        original_price_list.append(original_price)
        current_price_list.append(current_price)
        discount_list.append(discount)
        total_price_list.append(total_price)
        shipping_price_list.append(shipping_price)
        model_code_list.append(model_code)
        steering_list.append(steering)
        fuel_list.append(fuel)
        seats_list.append(seats)
        engine_code_list.append(engine_code)
        color_list.append(color)
        drive_list.append(drive)
        doors_list.append(doors)
        auction_grade_list.append(auction_grade)
    except Exception as e:
        errors.append(e)
        pass

data = {"vehicle_url": vehicle_url_list,
        "car_model":car_model_list,
        "mileage":mileage_list,
        "year":year_list,
        "engine":engine_list,
        "location":location_list,
        "original_price":original_price_list,
        "current_price":current_price_list,
        "discount":discount_list,
        "total_price":total_price_list,
        "shipping_price":shipping_price_list,
        "model_code":model_code_list,
        "steering":steering_list,
        "fuel":fuel_list,
        "seats":seats_list,
        "engine_code":engine_code_list,
        "color":color_list,
        "drive":drive_list,
        "doors":doors_list,
        "auction_grade":auction_grade_list}

df = pd.DataFrame(data)
#print(df)

excel_filename = 'JDM_Data.xlsx'
df.to_excel(excel_filename, index=False)

#print("\n\nErrors:", errors)
# with open("offers.txt", 'w', encoding='utf-8') as o:
#     o.write(str(car_offers[0]))
