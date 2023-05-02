import os
import pandas as pd

def make_hyperlink(value):
    url = "https:/{}"
    return '=HYPERLINK("%s", "%s")' % (url.format(value), value)

def create_dataframe(data):
    # create dataframe from dict
    df = pd.DataFrame(data)
    df['URL'] = df['URL'].apply(make_hyperlink)
    return df

def create_directory(excel_directory):
     if not os.path.exists(excel_directory):
          os.makedirs(excel_directory)

def save_to_excel(writer, dataframe, sheet_name):
    # Create directory if one does not exist
    dataframe.to_excel(writer, index=False, sheet_name = sheet_name)

def average_price_per_model_code(dataframe):
    avg_price_per_model = dataframe.groupby(["Model Code"]).aggregate({"Total Price USD":'mean', 'Model': 'max', "Color" : 'count'})
    avg_price_per_model = avg_price_per_model.astype({"Total Price USD": int})
    return avg_price_per_model