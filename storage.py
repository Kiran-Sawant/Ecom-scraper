import pandas as pd
from typing import List

from db import connection

def list_to_df(details:List[dict]):

    new_df = pd.DataFrame(details)

    return new_df

def df_to_csv(df:pd.DataFrame, path:str="my_csv"):
    
    df.to_csv(path, index=False)

def df_to_sql(df:pd.DataFrame, table_name:str , exists:str="replace"):

    df.to_sql(table_name, connection, index=False, if_exists=exists)
