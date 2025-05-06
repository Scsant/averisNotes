

from streamlit.runtime.uploaded_file_manager import UploadedFile
import streamlit as st
from typing import List, Union, Any
import pandas as pd

def load_averis_file(file: Union[str, Any]) -> pd.DataFrame:
    df = pd.read_excel(file, engine="openpyxl")
    df.dropna(axis=1, how='all', inplace=True)
    return df

def load_fazendas_files(files: List[Union[str, Any]]) -> List[pd.DataFrame]:
    dataframes = []
    for file in files:
        df = pd.read_excel(file, engine="openpyxl")
        df.columns = df.columns.str.strip()
        dataframes.append(df)
    return dataframes



