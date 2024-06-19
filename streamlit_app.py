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
from datetime import datetime


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

KEY ={
    "type": "service_account",
    "project_id": st.secrets["project_id"],
    "private_key_id": st.secrets["private_key_id"],
    "private_key": st.secrets["private_key"],
    "client_email": st.secrets["client_email"],
    "client_id": st.secrets["client_id"],
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://accounts.google.com/o/oauth2/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": st.secrets["client_x509_cert_url"],
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

st.image(Image.open("BD CAPITAL.png"))


name=st.text_input("Nombre")
password=st.text_input("Contraseña",type="password")
fecha=datetime.today().isoformat()

matches = [
    ("Argentina", "Canada", "empate", "jue. 20 jun. 19:00"),
    ("Peru", "Chile", "empate", "vie. 21 jun. 19:00"),
    ("Peru", "Canada", "empate", "lun. 24 jun. 17:00"),
    ("Chile", "Argentina", "empate", "mar. 25 jun. 20:00"),
    ("Argentina", "Peru", "empate", "sáb. 29 jun. 19:00"),
    ("Canada", "Chile", "empate", "sáb 29 jun. 19:00"),
    ("Ecuador", "Venezuela", "empate", "sáb. 22 jun. 17:00"),
    ("Mexico", "Jamaica", "empate", "sáb. 22 jun. 20:00"),
    ("Ecuador", "Jamaica", "empate", "mié. 26 jun. 17:00"),
    ("Venezuela", "Mexico", "empate", "mié. 26 jun. 20:00"),
    ("Mexico", "Ecuador", "empate", "dom. 30 jun. 19:00"),
    ("Jamaica", "Venezuela", "empate", "dom 30 jun. 19:00"),
    ("EE.UU.", "Bolivia", "empate", "dom. 23 jun. 17:00"),
    ("Uruguay", "Panama", "empate", "dom. 23 jun. 20:00"),
    ("Panama", "EE.UU.", "empate", "jue. 27 jun. 17:00"),
    ("Uruguay", "Bolivia", "empate", "jue. 27 jun. 20:00"),
    ("Bolivia", "Panama", "empate", "lun. 1 jul. 19:00"),
    ("EE.UU.", "Uruguay", "empate", "lun 1 jul. 19:00"),
    ("Colombia", "Paraguay", "empate", "lun 24 jun. 17:00"),
    ("Paraguay", "CostaRica", "empate", "mar. 25 jun. 18:00"),
    ("Colombia", "CostaRica", "empate", "vie. 28 jun. 17:00"),
    ("Paraguay", "Brasil", "empate", "sáb. 29 jun. 20:00"),
    ("Brasil", "Colombia", "empate", "mar. 2 jul. 19:00"),
    ("CostaRica", "Paraguay", "empate", "mar 2 jul. 19:00")
]

matches_flag = pd.DataFrame(matches, columns=["0", "1","2", "date"])

tab1,tab2=st.tabs(["Fijas","Verificar"])
with tab1:
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

    # Load images for Grupo C
    Uruguay = Image.open("paises/Grupo C/160_uruguay_150x100.png")
    Bolivia = Image.open("paises/Grupo C/164_bolivia_150x100.png")
    USA = Image.open("paises/Grupo C/1439_estados-unidos_150x100.png")
    Panama = Image.open("paises/Grupo C/19699_panama_150x100.png")

    # Load images for Grupo D
    Colombia = Image.open("paises/Grupo D/159_colombia_150x100.png")
    Brasil = Image.open("paises/Grupo D/165_brasil_150x100.png")
    Paraguay = Image.open("paises/Grupo D/168_paraguay_150x100.png")
    CostaRica = Image.open("paises/Grupo D/1431_costa-rica_150x100.png")

    # Initialize dictionaries to store selected values for each group
    selected_values_a = {}
    selected_values_b = {}
    selected_values_c = {}
    selected_values_d = {}

    propartido=df[df["Nombre"]==name].iloc[:,3:27].T.values.tolist()

    pronostico_first = pd.DataFrame({
    'date': matches_flag["date"],
    'Pronostico': propartido
    })

    pronostico_unpivoted = matches_flag.melt(id_vars=["date"], value_vars=["0", "1","2"], var_name="value", value_name="team")

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
                try:
                    x=pronostico_first.loc[pronostico_first["date"] == date_time, 'Pronostico'].values[0][0]
                    y_1=pronostico_unpivoted[pronostico_unpivoted['date']==date_time]
                    y=y_1.loc[y_1['team']==x,'value'].values[0][0]
                    #st.write(y)
                    #---------------                
                    selected_value = st.radio("", [team1_name, team2_name,"empate"], index=int(y), key=date_time, horizontal=True)
                    selected_values[date_time] = selected_value
                except:             
                    selected_value = st.radio("", [team1_name, team2_name,"empate"], index=0, key=date_time, horizontal=True)
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



    # Reset selected values for Grupo C
    selected_values_c = {}

    # Grupo C matches
    st.title("Grupo C")
    matches_C = [
        (USA, "EE.UU.", Bolivia, "Bolivia", "dom. 23 jun. 17:00"),
        (Uruguay, "Uruguay", Panama, "Panama", "dom. 23 jun. 20:00"),
        (Panama, "Panama", USA, "EE.UU.", "jue. 27 jun. 17:00"),
        (Uruguay, "Uruguay", Bolivia, "Bolivia", "jue. 27 jun. 20:00"),
        (Bolivia, "Bolivia", Panama, "Panama", "lun. 1 jul. 19:00"),
        (USA, "EE.UU.", Uruguay, "Uruguay", "lun 1 jul. 19:00")
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



    # Reset selected values for Grupo D
    selected_values_d = {}

    # Grupo D matches
    st.title("Grupo D")
    matches_D = [
        (Colombia, "Colombia", Paraguay, "Paraguay", "lun 24 jun. 17:00"),
        (Brasil, "Paraguay", CostaRica, "CostaRica", "mar. 25 jun. 18:00"),
        (Colombia, "Colombia", CostaRica, "CostaRica", "vie. 28 jun. 17:00"),
        (Paraguay, "Paraguay", Brasil, "Brasil", "sáb. 29 jun. 20:00"),
        (Brasil, "Brasil", Colombia, "Colombia", "mar. 2 jul. 19:00"),
        (CostaRica, "CostaRica", Paraguay, "Paraguay", "mar 2 jul. 19:00")
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


    grupo_a_valor=list(selected_values_a.values())
    grupo_b_valor=list(selected_values_b.values())
    grupo_c_valor=list(selected_values_c.values())
    grupo_d_valor=list(selected_values_d.values())


    try:
        nombres_index=df[df['Nombre']== name].index[0] #sumar +2 en el excel
    except:
        nombres_index=maxrow

    #st.write(nombres_index)


    try:
        password_check=df[df["Password"]==password].index[0]
    except:
        password_check=nombres_index

    if nombres_index<maxrow:
        if password_check==nombres_index:
            Rangea=f"polla!D{nombres_index+2}"
            valores=grupo_a_valor+grupo_b_valor+grupo_c_valor+grupo_d_valor
            def fill(valores,rangea):
                filling = service.spreadsheets().values().update(
                spreadsheetId=SPREADSHEET_ID,
                range=rangea,
                valueInputOption='USER_ENTERED',
                body={'values': [valores]}
                )
                return filling.execute()
        else:
            st.title('Contraseña incorrecta')

    elif nombres_index==maxrow:
        Rangea=f"polla!A{nombres_index}"
        valores=[name]+[password]+[fecha]+grupo_a_valor+grupo_b_valor+grupo_c_valor+grupo_d_valor
        def fill(valores,rangea):
            filling = service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=rangea,
            valueInputOption='USER_ENTERED',
            body={'values': [valores]}
            )
            return filling.execute()




    boton_fill=st.button("Entrar", on_click=fill, args=(valores,Rangea,))







    st.image(Image.open("FIXTURE.png"))

with tab2:

    matches = [
    # Group A
    "Argentina - Canada - jue. 20 jun. 19:00",
    "Peru - Chile - vie. 21 jun. 19:00",
    "Peru - Canada - lun. 24 jun. 17:00",
    "Chile - Argentina - mar. 25 jun. 20:00",
    "Argentina - Peru - sáb. 29 jun. 19:00",
    "Canada - Chile - sáb 29 jun. 19:00",
    
    # Group B
    "Ecuador - Venezuela - sáb. 22 jun. 17:00",
    "Mexico - Jamaica - sáb. 22 jun. 20:00",
    "Ecuador - Jamaica - mié. 26 jun. 17:00",
    "Venezuela - Mexico - mié. 26 jun. 20:00",
    "Mexico - Ecuador - dom. 30 jun. 19:00",
    "Jamaica - Venezuela - dom 30 jun. 19:00",
    
    # Group C
    "USA - Bolivia - dom. 23 jun. 17:00",
    "Uruguay - Panama - dom. 23 jun. 20:00",
    "Panama - USA - jue. 27 jun. 17:00",
    "Uruguay - Bolivia - jue. 27 jun. 20:00",
    "Bolivia - Panama - lun. 1 jul. 19:00",
    "USA - Uruguay - lun 1 jul. 19:00",
    
    # Group D
    "Colombia - Paraguay - lun 24 jun. 17:00",
    "Brasil - CostaRica - mar. 25 jun. 18:00",
    "Colombia - CostaRica - vie. 28 jun. 17:00",
    "Paraguay - Brasil - sáb. 29 jun. 20:00",
    "Brasil - Colombia - mar. 2 jul. 19:00",
    "CostaRica - Paraguay - mar 2 jul. 19:00"
    ]


    check=df[df['Nombre']==name].iloc[:,3:27]
    check_T=check.T.values.tolist()

    pronostico = pd.DataFrame({
    'Partidos': matches,
    'Pronóstico': check_T
    })

    st.table(pronostico)