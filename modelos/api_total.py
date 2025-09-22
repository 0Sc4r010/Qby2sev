import requests
import pandas as pd
from datetime import datetime
from requests.auth import HTTPBasicAuth
import xml.etree.ElementTree as ET

from modelos.data_access import process_tickes, process_view


def process_api(ahora): 

    # URL del API
    url = "http://integrabolivariano.rjconsultores.com.br/RJIntegra/rest/padrao/tiquetesVendidos"
   
    params = {
        "idEmpresa": 42,
        "fechaInicio": ahora.strftime("%y%m%d") + "0000",
        "fechaFinalizacion": ahora.strftime("%y%m%d") + "2359"
    }
    
  
    
    # Credenciales
    usuario = "bolivariano"
    contrasena = "bolivariano2024"


    try:
        response = requests.get(url, params=params, auth=HTTPBasicAuth(usuario, contrasena))
        
        # Realizar la solicitud
        response.raise_for_status()
        # Parsear el XML
        xml_data = response.text
        root = ET.fromstring(xml_data)

    # Extraer datos de <tiqueteVendido>
        tiquetes = []
        for elem in root.findall(".//tiqueteVendido"):
            tiquete = {}
            for child in elem:
                if child.tag == "formaDePagos":
                   pago_dict = {sub.tag: sub.text for sub in child}
                   tiquete["formaDePagos"] = pago_dict
                else:
                   tiquete[child.tag] = child.text
            tiquetes.append(tiquete)
        
        df = pd.DataFrame(tiquetes)
        df["fechaDeVenta"] = pd.to_datetime(df["fechaDeVenta"]).dt.date
        print(df.head())
        for _, row in df.iterrows():
            print(row.get("idEmpresa", 0))
            process_tickes(row)
        process_view(ahora)
        

        # Si deseas guardar en Excel:
        # df.to_excel("tiquetes_vendidos2.xlsx", index=False)

    except requests.RequestException as e:
        print("Error en la solicitud:", e)
    except ValueError as e:
        print("Error al procesar JSON:", e)
