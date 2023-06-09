import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
from timeit import default_timer as timer
from datetime import timedelta
import helper_functions

# get the number of pages to loops through (extract the highest number from pagination buttons)
def get_number_of_pages(first_page_soup):
    pagination_numbers = []
    amount_of_pages = 0
    pagination_div = first_page_soup.find("div", class_="results-pagination")
    pagination_li = pagination_div.find_all("li")
    for li in pagination_li:
        pagination_a = li.find("a")
        try: 
            pagination_numbers.append(int(pagination_a.contents[0]))
        except Exception as e:
            logging.exception('Error raised')
            pass
    for n in pagination_numbers:
        if n > amount_of_pages:
            amount_of_pages = n

    return amount_of_pages


# Initialize empty lists to be used in creating pandas dataframe
def scrape(pages_to_loop_through):
    homepage_url = 'beforward.jp'
    execution_log = f'Starting Scraping\n\nPages to go through: {pages_to_loop_through}\n\n'
    offers_count = 0
    error_offers_count = 0
    vehicle_id_list = []
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
    transmission_list = []
    fuel_list =[]
    seats_list =[]
    engine_code_list =[]
    color_list =[]
    drive_list =[]
    doors_list =[]
    auction_grade_list =[]
    current_page_number = 0

    timer_start = timer()

    for p in range(pages_to_loop_through):
        current_page_number += 1
        current_page_errors = 0
        scraping_page_number_message = 'Scraping Page Number: ' + str(current_page_number) +'\n'
        print(scraping_page_number_message)
        execution_log += scraping_page_number_message
        current_url = f'https://www.beforward.jp/stocklist/icon_clearance=1/page={current_page_number}/sortkey=q'
        current_page = requests.get(current_url)
        current_page_soup = BeautifulSoup(current_page.content, "html.parser")

        # offers box
        all_offers = current_page_soup.find("div", class_="cars-box-stocklist-renewal")

        # offers box more specific
        car_offers = all_offers.find_all("tr", class_="stocklist-row")

        # loop over car offers and extract vehicle parameters
        for car_offer in car_offers:
            offers_count += 1
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
                mileage = int(mileage_td.find("p", class_='val').contents[0].strip().replace("km", "").replace(',', ''))
                date_td = car_offer.find("td", class_ = "basic-spec-col basic-spec-col-bordered year")
                date = date_td.find("p", class_='val').contents[0].strip()
                year = date[0:4]
                engine_td = car_offer.find("td", class_ = "basic-spec-col basic-spec-col-bordered engine")
                engine = engine_td.find("p", class_='val').contents[0].strip().replace("cc", "")
                location_td = car_offer.find("p", class_ = "val stock-area")
                location = location_td.find("span").contents[0].strip()
                original_price = int(car_offer.find("p", class_ = "original-vehicle-price").contents[0].strip().replace(',', ''))
                current_price =  int(car_offer.find("span", class_ = "price").contents[0].strip().replace('$', '').replace(",", ''))
                discount = car_offer.find("p", class_ = "save-rate").contents[0].strip().replace("%", "")
                total_price_p = car_offer.find("p", class_ = "total-price")
                total_price = int(total_price_p.find("span", class_=None).contents[0].strip().replace('$', '').replace(",", ''))
                shipping_price = total_price - current_price

                transmission_td = car_offer.find("td", class_ = "basic-spec-col basic-spec-col-bordered trans")
                transmission = transmission_td.find("p", class_='val').contents[0].strip()

                if transmission == 'AT':
                    transmission = 'Automatic'
                if transmission == 'MT':
                    transmission = "Manual"
                
                table_detailed_spec = car_offer.find("table", class_ = "table-detailed-spec")
                table_rows = table_detailed_spec.find_all("tr")
                first_row = table_rows[0]
                second_row = table_rows[1]
                try:
                    third_row = table_rows[2]
                    auction_grade = third_row.find("td", class_="td-colspan").contents[0].strip()
                except:
                    auction_grade = 'None'

                model_code = first_row.find("td", class_="td-1st").contents[0].strip()
                steering = first_row.find("td", class_="td-2nd").contents[0].strip()
                fuel = first_row.find("td", class_="td-3rd").contents[0].strip()
                seats = first_row.find("td", class_="td-4th").contents[0].strip()

                engine_code = second_row.find("td", class_="td-1st").contents[0].strip()
                color = second_row.find("td", class_="td-2nd").contents[0].strip()
                drive = second_row.find("td", class_="td-3rd").contents[0].strip()
                doors = second_row.find("td", class_="td-4th").contents[0].strip()

                
                
                # Log vehicle data
                
                # print('\n\nSaving to excel:')
                # print(vehicle_id)
                # print(vehicle_url)
                # print(car_model)
                # print(mileage)
                # print(year)

                # print(engine)
                # print(location)
                # print(original_price)
                # print(current_price)
                # print(discount)
                # print(total_price)
                # print(shipping_price)
                # print(model_code)
                # print(steering)
                # print(transmission)
                # print(fuel)
                # print(seats)
                # print(engine_code)
                # print(color)
                # print(drive)
                # print(doors)
                # print(auction_grade)
                # print("\n\n")
                
                # append data to lists
                vehicle_id_list.append(vehicle_id)
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
                transmission_list.append(transmission)
                fuel_list.append(fuel)
                seats_list.append(seats)
                engine_code_list.append(engine_code)
                color_list.append(color)
                drive_list.append(drive)
                doors_list.append(doors)
                auction_grade_list.append(auction_grade)
            except Exception as e:
                logging.exception('Error raised')
                error_offers_count += 1
                current_page_errors += 1
        execution_log += f'\tErrors on page: {current_page_errors}\n'

        timer_end = timer()

    time_spent_on_scraping = helper_functions.format_time(seconds=timer_end-timer_start)
    time_spent_scraping_message = "\nTime spent scraping: " + str(time_spent_on_scraping) + '\n'
    average_time_scraping_per_page_message = "Average time per page: " + str(round(((timer_end - timer_start) / pages_to_loop_through), 2)) + "s\n\n"
    print(time_spent_scraping_message)
    execution_log += time_spent_scraping_message
    print(average_time_scraping_per_page_message)
    execution_log += average_time_scraping_per_page_message 
    execution_log += f"Errors Encountered: {error_offers_count}\n"
    execution_log += f"Number of offers successfully scraped: {offers_count - error_offers_count}\n"


    # define data dictionary
    data = {"Vehicle ID":vehicle_id_list,
            "Model":car_model_list,
            "Mileage (km)":mileage_list,
            "Engine (cc)":engine_list,
            "Year":year_list,
            "Auction Grade":auction_grade_list,
            "Steering":steering_list,
            "Transmission":transmission_list,
            "Total Price USD":total_price_list,
            "Original Price USD":original_price_list,
            "Current Price USD":current_price_list,
            "Discount %":discount_list,
            "Shipping Price USD":shipping_price_list,
            "Location":location_list,
            "Model Code":model_code_list,
            "Fuel":fuel_list,
            "Seats":seats_list,
            "Engine Code":engine_code_list,
            "Color":color_list,
            "Drive":drive_list,
            "Doors":doors_list,
            "URL": vehicle_url_list
    }

    return data, execution_log
