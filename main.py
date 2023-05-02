import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import date
import os
import logging
from scraping import get_number_of_pages, scrape
import excel_statistics
import helper_functions



# Directory/File paths 
today = str(date.today()).replace('-', '_')

script_dir = str(os.path.dirname(os.path.abspath(__file__)))
logs_folder_dir = script_dir + '/Logs'

error_logs_folder_dir = logs_folder_dir + '/Error'
error_log_filename = error_logs_folder_dir + f'/error_log_{today}.txt'

execution_logs_folder_dir = logs_folder_dir + '/Execution/'
execution_log_filename = execution_logs_folder_dir + f'/execution_log_{today}.txt'

excel_directory = script_dir + '/JDM_DATA'
excel_filename = '/JDM_DATA_' + today + '.xlsx'
excel_absolute_path = excel_directory + excel_filename

# Create log directories if not exist
helper_functions.create_directory(logs_folder_dir)
helper_functions.create_directory(error_logs_folder_dir)
helper_functions.create_directory(execution_logs_folder_dir)

# Clear error log file
with open(error_log_filename, 'w'):
    pass

# Create execution log file and string
execution_log_contents = 'Starting Scripts\n\n'
execution_log_file = open(execution_log_filename, 'w')

# enable logging
logging.basicConfig(filename=error_log_filename, level=logging.DEBUG)

first_url = 'https://www.beforward.jp/stocklist/icon_clearance=1/page=1/sortkey=q'
first_page = requests.get(first_url)
first_page_soup = BeautifulSoup(first_page.content, "html.parser")

amount_of_pages = get_number_of_pages(first_page_soup)

if __name__ == "__main__":

    # scrape data, create dataframe
    scrape_returned_data = scrape(pages_to_loop_through = 5)
    data = scrape_returned_data[0]
    scraping_execution_log = scrape_returned_data[1]
    execution_log_contents += scraping_execution_log

    dataframe = excel_statistics.create_dataframe(data)

    # Create directory if not exists
    helper_functions.create_directory(excel_directory)

    # Write to excel sheets
    with pd.ExcelWriter(excel_absolute_path) as writer:
        execution_log_contents += r"Creating Sheet = 'carData'"
        execution_log_contents += '\n'
        excel_statistics.save_to_excel(writer, dataframe, sheet_name="carData")
        avg_price_per_model = excel_statistics.average_price_per_model_code(dataframe)
        execution_log_contents += r"Creating Sheet = 'Statistics'"
        execution_log_contents += '\n'
        excel_statistics.save_to_excel(writer, avg_price_per_model, sheet_name="Statistics")
    
    execution_log_file.write(execution_log_contents)

execution_log_file.close()
