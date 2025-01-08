import streamlit as st
import requests
from urllib.parse import urlencode
import os
from dotenv import load_dotenv

# Preset requests
POSSIBLE_REQUESTS = {
    "nursing": [
        "Solicitar Medicação para Dor",
        "Solicitar Verificação de Soro",
        "Solicitar Verificação de Sinais Vitais",
        "Solicitar Assistência para Mobilidade",
        "Solicitar Troca de Curativo",
        "Solicitar Consulta Médica",
    ],
    "cleaning": [
        "Solicitar Limpeza do Quarto",
        "Solicitar Limpeza do Banheiro",
        "Solicitar Manutenção da Cama",
        "Solicitar Reparo na Iluminação",
        "Solicitar Ajuste no Ar-Condicionado",
        "Solicitar Remoção do Lixo",
    ],
}

# API endpoint for requests
load_dotenv()
API_ENDPOINT = os.getenv("API_ENDPOINT") 

# Extract bed_id from query params
bed_id = st.experimental_get_query_params().get("bed_id", [None])[0]
if not bed_id:
    st.error("Nenhum ID de Leito fornecido. Acesse esta página através de um código QR válido.")
    st.stop()

# Page title
st.title("Solicitações para o Leito")
st.subheader(f"ID do Leito: {bed_id}")

# Function to send POST request to API
def send_request_to_api(bed_id, request_id):
    payload = {"bed_id": bed_id, "request_id": request_id}
    try:
        response = requests.post(API_ENDPOINT, json=payload)
        if response.status_code == 200:
            st.success(f"Solicitação '{request_id}' enviada com sucesso!")
        else:
            st.error(f"Erro ao enviar a solicitação: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"Erro ao se conectar à API: {e}")

# User interface for making requests
st.write("Selecione uma categoria de solicitação:")
category = st.radio("Categoria", list(POSSIBLE_REQUESTS.keys()), format_func=lambda x: x.capitalize())

if category:
    st.write("Selecione uma solicitação:")
    for request_id in POSSIBLE_REQUESTS[category]:
        if st.button(request_id):
            send_request_to_api(bed_id, request_id)
    outro = st.text_area("Outro", height=68)
    if st.button("Enviar"):
        send_request_to_api(bed_id, outro)  

