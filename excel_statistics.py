import os
import pandas as pd
import helper_functions

def create_dataframe(data):
    # create dataframe from dict
    df = pd.DataFrame(data)
    df['URL'] = df['URL'].apply(helper_functions.make_hyperlink)
    return df

def create_directory(directory):
     if not os.path.exists(directory):
          os.makedirs(directory)

def save_to_excel(writer, dataframe, sheet_name):
    # Create directory if one does not exist
    dataframe.to_excel(writer, index=False, sheet_name = sheet_name)

def average_price_per_model_code(dataframe):
    avg_price_per_model = dataframe.groupby(["Model Code"]).aggregate({'Model': 'max', "Model Code":'max', "Total Price USD":'mean',  "Color" : 'count'})
    avg_price_per_model = avg_price_per_model.astype({"Total Price USD": int})
    avg_price_per_model.rename(columns = {'Color':'Model Count', 'Total Price USD':'Average Price USD', 'Model Code':'ModelCode'}, inplace=True)
    avg_price_per_model_final = avg_price_per_model.where(avg_price_per_model.ModelCode != 0)
    return avg_price_per_model_final