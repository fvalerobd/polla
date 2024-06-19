import os
from datetime import datetime
import time
import pandas as pd
from copy import copy
from pathlib import Path
import re
import numpy as np
import sys
import streamlit as st
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account
import random
import plotly.express as px
import plotly.graph_objects as go
import json
from PIL import Image

json_file_path = 'pollabd-fb6841ee6be0.json'

with open(json_file_path, 'r') as file:
    data = json.load(file)

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

KEY ={
    "type": "service_account",
    "project_id": data["project_id"],
    "private_key_id": data["private_key_id"],
    "private_key": data["private_key"],
    "client_email": data["client_email"],
    "client_id": data["client_id"],
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://accounts.google.com/o/oauth2/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": data["client_x509_cert_url"],
    "universe_domain": "googleapis.com"
}

SPREADSHEET_ID = '1vAY13hq7-V4zO6UMkMyJmYYrheXBC9G26maf5EazxMQ'
RANGE_NAME_GET="polla!A:AI"

creds = None
creds = service_account.Credentials.from_service_account_info(KEY, scopes=SCOPES)

service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

result = (
        sheet.values()
        .get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME_GET)
        .execute()
    )

values = result.get('values',[])
df=pd.DataFrame(values[1:], columns=values[0])
df_fix=df[df["Nombre"] != '']
df_index=df_fix.index
maxrow=df_index[-1]+3

RANGE_NAME_FILL=f"polla!A{maxrow}"

def llenar(valores,rangea):
    filling = service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=rangea,
        valueInputOption='USER_ENTERED',
        body={'values': [valores]}
    )
    return filling.execute()

def actualizar(valores,rangea):
    filling = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=rangea,
        valueInputOption='USER_ENTERED',
        body={'values': [valores]}
    )
    return filling.execute()

'''Argentina = Image.open("paises/Grupo A/163_argentina_150x100.png")
Canada = Image.open("paises/Grupo A/1429_canada_150x100.png")
Peru = Image.open("paises/Grupo A/169_peru_150x100.png")
Chile = Image.open("paises/Grupo A/162_chile_150x100.png")

selected_values = []

def create_match_container(team1_img, team1_name, team2_img, team2_name, date_time):
    global selected_values

    with st.container():
        st.write(date_time)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            st.image(team1_img, width=50)
        with col2:
            selected_value = st.radio("", [team1_name, team2_name], index=0, key=date_time,horizontal=True)
            selected_values.append(selected_value)
        with col3:
            st.image(team2_img, width=50)

st.title("Grupo A")

matches_A = [
    (Argentina, "Argentina", Canada, "Canada", "jue. 20 jun. 19:00"),
    (Peru, "Peru", Chile, "Chile", "vie. 21 jun. 19:00"),
    (Peru, "Peru", Canada, "Canada", "lun. 24 jun. 17:00"),
    (Chile, "Chile", Argentina, "Argentina", "mar. 25 jun. 20:00"),
    (Argentina, "Argentina", Peru, "Peru", "sáb. 29 jun. 19:00"),
    (Canada, "Canada", Chile, "Chile", "sáb 29 jun. 19:00")
]

for match in matches_A:
    create_match_container(*match)

Group_a=selected_values

st.write(selected_values)
#--------------------------------

Venezuela = Image.open("paises/Grupo B/161_venezuela_150x100.png")
Ecuador = Image.open("paises/Grupo B/166_ecuador_150x100.png")
Mexico = Image.open("paises/Grupo B/1435_mexico_150x100.png")
Jamaica = Image.open("paises/Grupo B/19700_jamaica_150x100.png")




st.title("Grupo B")

matches_B = [
    (Ecuador, "Ecuador", Venezuela, "Venezuela", "sáb. 22 jun. 17:00"),
    (Mexico, "Mexico", Jamaica, "Jamaica", "sáb. 22 jun. 20:00"),
    (Ecuador, "Ecuador", Jamaica, "Jamaica", "mié. 26 jun. 17:00"),
    (Venezuela, "Venezuela", Mexico, "Mexico", "mié. 26 jun. 20:00"),
    (Mexico, "Mexico", Ecuador, "Ecuador", "dom. 30 jun. 19:00"),
    (Jamaica, "Jamaica", Venezuela, "Venezuela", "dom 30 jun. 19:00")
]

selected_values = []
for match in matches_B:
    create_match_container(*match)

Group_b=selected_values'''

# Load images for Grupo A
Argentina = Image.open("paises/Grupo A/163_argentina_150x100.png")
Canada = Image.open("paises/Grupo A/1429_canada_150x100.png")
Peru = Image.open("paises/Grupo A/169_peru_150x100.png")
Chile = Image.open("paises/Grupo A/162_chile_150x100.png")

# Load images for Grupo B
Venezuela = Image.open("paises/Grupo B/161_venezuela_150x100.png")
Ecuador = Image.open("paises/Grupo B/166_ecuador_150x100.png")
Mexico = Image.open("paises/Grupo B/1435_mexico_150x100.png")
Jamaica = Image.open("paises/Grupo B/19700_jamaica_150x100.png")

'''# Load images for Grupo C
Italy = Image.open("paises/Grupo C/italy.png")
France = Image.open("paises/Grupo C/france.png")
Brazil = Image.open("paises/Grupo C/brazil.png")
Germany = Image.open("paises/Grupo C/germany.png")

# Load images for Grupo D
Spain = Image.open("paises/Grupo D/spain.png")
England = Image.open("paises/Grupo D/england.png")
Netherlands = Image.open("paises/Grupo D/netherlands.png")
Portugal = Image.open("paises/Grupo D/portugal.png")'''

# Initialize dictionaries to store selected values for each group
selected_values_a = {}
selected_values_b = {}
selected_values_c = {}
selected_values_d = {}

def create_match_container(group, team1_img, team1_name, team2_img, team2_name, date_time):
    global selected_values_a, selected_values_b, selected_values_c, selected_values_d

    # Choose the appropriate selected_values dictionary based on the group
    if group == 'A':
        selected_values = selected_values_a
    elif group == 'B':
        selected_values = selected_values_b
    elif group == 'C':
        selected_values = selected_values_c
    elif group == 'D':
        selected_values = selected_values_d

    with st.container():
        # Row 1
        st.write(date_time)
        row1 = st.columns([3, 3])
        
        with row1[0]:
            st.image(team1_img, width=50)
        with row1[1]:
            st.image(team2_img, width=50)

        # Row 2
        row2 = st.columns([1, 10, 1])
        with row2[1]:
            selected_value = st.radio("", [team1_name, team2_name], index=0, key=date_time, horizontal=True)
            selected_values[date_time] = selected_value

# Grupo A matches
st.title("Grupo A")
matches_A = [
    (Argentina, "Argentina", Canada, "Canada", "jue. 20 jun. 19:00"),
    (Peru, "Peru", Chile, "Chile", "vie. 21 jun. 19:00"),
    (Peru, "Peru", Canada, "Canada", "lun. 24 jun. 17:00"),
    (Chile, "Chile", Argentina, "Argentina", "mar. 25 jun. 20:00"),
    (Argentina, "Argentina", Peru, "Peru", "sáb. 29 jun. 19:00"),
    (Canada, "Canada", Chile, "Chile", "sáb 29 jun. 19:00")
]

row1_A, c, row2_A, d, row3_A = st.columns([4, 1, 4, 1, 4])
for i in [0, 3]:
    with row1_A:
        create_match_container('A', *matches_A[i])
    with c:
        st.empty()  # Placeholder for the empty column
    with row2_A:
        create_match_container('A', *matches_A[i+1])
    with d:
        st.empty()  # Placeholder for the empty column
    with row3_A:
        create_match_container('A', *matches_A[i+2])

# Display selected values for Grupo A
st.write("Selected values - Grupo A:")
st.write(selected_values_a)

# Reset selected values for Grupo B
selected_values_b = {}

# Grupo B matches
st.title("Grupo B")
matches_B = [
    (Ecuador, "Ecuador", Venezuela, "Venezuela", "sáb. 22 jun. 17:00"),
    (Mexico, "Mexico", Jamaica, "Jamaica", "sáb. 22 jun. 20:00"),
    (Ecuador, "Ecuador", Jamaica, "Jamaica", "mié. 26 jun. 17:00"),
    (Venezuela, "Venezuela", Mexico, "Mexico", "mié. 26 jun. 20:00"),
    (Mexico, "Mexico", Ecuador, "Ecuador", "dom. 30 jun. 19:00"),
    (Jamaica, "Jamaica", Venezuela, "Venezuela", "dom 30 jun. 19:00")
]

row1_B, a, row2_B, b, row3_B = st.columns([4, 1, 4, 1, 4])
for i in [0, 3]:
    with row1_B:
        create_match_container('B', *matches_B[i])
    with a:
        st.empty()  # Placeholder for the empty column
    with row2_B:
        create_match_container('B', *matches_B[i+1])
    with b:
        st.empty()  # Placeholder for the empty column
    with row3_B:
        create_match_container('B', *matches_B[i+2])

# Display selected values for Grupo B
st.write("Selected values - Grupo B:")
st.write(selected_values_b)

# Reset selected values for Grupo C
selected_values_c = {}

# Grupo C matches
st.title("Grupo C")
matches_C = [
    (Italy, "Italy", France, "France", "dom. 23 jun. 18:00"),
    (Brazil, "Brazil", Germany, "Germany", "dom. 23 jun. 21:00"),
    (Italy, "Italy", Germany, "Germany", "jue. 27 jun. 18:00"),
    (France, "France", Brazil, "Brazil", "jue. 27 jun. 21:00"),
    (France, "France", Italy, "Italy", "lun. 1 jul. 18:00"),
    (Germany, "Germany", Brazil, "Brazil", "lun. 1 jul. 21:00")
]

row1_C, e, row2_C, f, row3_C = st.columns([4, 1, 4, 1, 4])
for i in [0, 3]:
    with row1_C:
        create_match_container('C', *matches_C[i])
    with e:
        st.empty()  # Placeholder for the empty column
    with row2_C:
        create_match_container('C', *matches_C[i+1])
    with f:
        st.empty()  # Placeholder for the empty column
    with row3_C:
        create_match_container('C', *matches_C[i+2])

# Display selected values for Grupo C
st.write("Selected values - Grupo C:")
st.write(selected_values_c)

# Reset selected values for Grupo D
selected_values_d = {}

# Grupo D matches
st.title("Grupo D")
matches_D = [
    (Spain, "Spain", England, "England", "sáb. 22 jun. 18:00"),
    (Netherlands, "Netherlands", Portugal, "Portugal", "sáb. 22 jun. 21:00"),
    (Spain, "Spain", Portugal, "Portugal", "mié. 26 jun. 18:00"),
    (England, "England", Netherlands, "Netherlands", "mié. 26 jun. 21:00"),
    (England, "England", Spain, "Spain", "dom. 30 jun. 18:00"),
    (Portugal, "Portugal", Netherlands, "Netherlands", "dom 30 jun. 21:00")
]

row1_D, g, row2_D, h, row3_D = st.columns([4, 1, 4, 1, 4])
for i in [0, 3]:
    with row1_D:
        create_match_container('D', *matches_D[i])
    with g:
        st.empty()  # Placeholder for the empty column
    with row2_D:
        create_match_container('D', *matches_D[i+1])
    with h:
        st.empty()  # Placeholder for the empty column
    with row3_D:
        create_match_container('D', *matches_D[i+2])

# Display selected values for Grupo D
st.write("Selected values - Grupo D:")
st.write(selected_values_d)