import numpy as np
import pandas as pd
import openpyxl
import streamlit as st
import streamlit.components.v1 as components
import json

##### Dataframe filter
def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    modify = st.checkbox("필터 추가")

    if not modify:
        return df
    df = df.copy()

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("다음 범주로 표를 간추립니다", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"{column}를 선택하세요.",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = int(df[column].min())
                _max = int(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"{column} 범위를 설정하세요.",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=1,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"{column} 범주를 선택하세요.",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"찾을 {column}을(를) 입력하세요.",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]

    return df


@st.cache_data
def load_data(url):
    df_full = pd.read_excel(url)
    df_full = df_full.fillna(np.nan)
    return df_full


df= load_data("lib230830.xlsx")
st.dataframe(filter_dataframe(df), use_container_width=True)


