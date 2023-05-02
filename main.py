import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import date
import os
import logging
from scraping import get_number_of_pages, scrape

script_dir = str(os.path.dirname(os.path.abspath(__file__)))
LOG_FILENAME = script_dir + '/error_log.txt'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)
today = str(date.today()).replace('-', '_')

first_url = 'https://www.beforward.jp/stocklist/icon_clearance=1/page=1/sortkey=q'
first_page = requests.get(first_url)
first_page_soup = BeautifulSoup(first_page.content, "html.parser")

amount_of_pages = get_number_of_pages(first_page_soup)

def make_hyperlink(value):
    url = "https:/{}"
    return '=HYPERLINK("%s", "%s")' % (url.format(value), value)

def create_dataframe(data):
    # create dataframe from dict
    df = pd.DataFrame(data)
    df['URL'] = df['URL'].apply(make_hyperlink)
    return df

def save_to_excel(dataframe, excel_directory, excel_filename):
    # Create directory if one does not exist
    if not os.path.exists(excel_directory):
          os.makedirs(excel_directory)
    excel_absolute_path = excel_directory + excel_filename
    dataframe.to_excel(excel_absolute_path, index=False, sheet_name = "carData")

if __name__ == "__main__":
    data = scrape(pages_to_loop_through = 2)
    dataframe = create_dataframe(data)
    excel_directory = script_dir + '/JDM_DATA/'
    excel_filename = 'JDM_DATA_' + today + '.xlsx'
    save_to_excel(dataframe, excel_directory, excel_filename)


