import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import date
import os
import logging
from scraping import get_number_of_pages, scrape
import excel_statistics


script_dir = str(os.path.dirname(os.path.abspath(__file__)))
LOG_FILENAME = script_dir + '/error_log.txt'

today = str(date.today()).replace('-', '_')
excel_directory = script_dir + '/JDM_DATA/'
excel_filename = 'JDM_DATA_' + today + '.xlsx'
excel_absolute_path = excel_directory + excel_filename


# Clear log file
with open(LOG_FILENAME, 'w'):
    pass

# enable logging
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

first_url = 'https://www.beforward.jp/stocklist/icon_clearance=1/page=1/sortkey=q'
first_page = requests.get(first_url)
first_page_soup = BeautifulSoup(first_page.content, "html.parser")

amount_of_pages = get_number_of_pages(first_page_soup)


if __name__ == "__main__":

    # scrape data, create dataframe
    data = scrape(pages_to_loop_through = 2)
    dataframe = excel_statistics.create_dataframe(data)

    # Create directory if not exists
    excel_statistics.create_directory(excel_directory)

    # Write to excel sheets
    with pd.ExcelWriter(excel_absolute_path) as writer:
        excel_statistics.save_to_excel(writer, dataframe, sheet_name="carData")
        avg_price_per_model = excel_statistics.average_price_per_model_code(dataframe)
        excel_statistics.save_to_excel(writer, avg_price_per_model, sheet_name="statistics")


