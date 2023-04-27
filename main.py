import requests
from bs4 import BeautifulSoup
import pandas as pd

errors = []
homepage_url = 'beforward.jp'

first_url = 'https://www.beforward.jp/stocklist/icon_clearance=1/page=1/sortkey=q'


first_page = requests.get(first_url)
first_page_soup = BeautifulSoup(first_page.content, "html.parser")

# get the number of pages to loops through (extract the highest number from pagination buttons)
pagination_numbers = []
amount_of_pages = 0
pagination_div = first_page_soup.find("div", class_="results-pagination")
pagination_li = pagination_div.find_all("li")
for li in pagination_li:
    pagination_a = li.find("a")
    try: 
        pagination_numbers.append(int(pagination_a.contents[0]))
    except Exception as e:
        errors.append(e)
        pass

for n in pagination_numbers:
        if n > amount_of_pages:
            amount_of_pages = n

# Initialize empty lists to be used in creating pandas dataframe
vehicle_id_list = []
vehicle_url_list = []
car_model_list =[]
mileage_list =[]
year_list =[]
month_list = []
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



def scrape(display_all_data = 0, pages_to_loop_through = amount_of_pages, display_errors = 0):
    current_page_number = 0
    for p in range(pages_to_loop_through):
        current_page_number += 1
        print('\nScraping Page Number ', str(current_page_number), '\n')
        current_url = f'https://www.beforward.jp/stocklist/icon_clearance=1/page={current_page_number}/sortkey=q'
        current_page = requests.get(current_url)
        current_page_soup = BeautifulSoup(current_page.content, "html.parser")



        # offers box
        all_offers = current_page_soup.find("div", class_="cars-box-stocklist-renewal")

        # offers box more specific
        car_offers = all_offers.find_all("tr", class_="stocklist-row")

        # loop over car offers and extract vehicle parameters
        for car_offer in car_offers:
            try:
                vehicle_id_p = car_offer.find("p", class_="veh-stock-no")
                vehicle_id = vehicle_id_p.find("span").contents[0].replace("Ref No. ", "")
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
                date_td = car_offer.find("td", class_ = "basic-spec-col basic-spec-col-bordered year")
                date = date_td.find("p", class_='val').contents[0].strip()
                year = date[0:4]
                month = date[5:]
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
                
                # display helpful data 
                if display_all_data == 1:
                    print('\n\nSaving to excel:')
                    print(vehicle_id)
                    print(vehicle_url)
                    print(car_model)
                    print(mileage)
                    print(year)
                    print(month)
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
                
                # append data to lists
                vehicle_id_list.append(vehicle_id)
                vehicle_url_list.append(vehicle_url)
                car_model_list.append(car_model)
                mileage_list.append(mileage)
                year_list.append(year)
                month_list.append(month)
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
    

    if display_errors == 1:
        print(errors)

    # define data dictionary
    data = {"vehicle_id":vehicle_id_list,
            "car_model":car_model_list,
            "mileage":mileage_list,
            "engine":engine_list,
            "year":year_list,
            "auction_grade":auction_grade_list,
            "steering":steering_list,
            "total_price":total_price_list,
            #"month":month_list,
            "original_price":original_price_list,
            "current_price":current_price_list,
            "discount":discount_list,
            "shipping_price":shipping_price_list,
            "location":location_list,
            "model_code":model_code_list,
            "fuel":fuel_list,
            "seats":seats_list,
            "engine_code":engine_code_list,
            "color":color_list,
            "drive":drive_list,
            "doors":doors_list,
            "vehicle_url": vehicle_url_list
    }

    # create dataframe from dict, save to excel
    df = pd.DataFrame(data)
    excel_filename = 'JDM_Data.xlsx'
    df.to_excel(excel_filename, index=False, sheet_name = "carData")


scrape(pages_to_loop_through = 3)