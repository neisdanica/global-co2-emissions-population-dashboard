import pandas as pd 

def clean_data(file_path):

    # Load the dataset
    df = pd.read_csv(file_path)

    # Cleaning the data. Removing non-country data. 
    df_cleaned =df.dropna(subset=['iso_code']).copy()

    return df_cleaned

