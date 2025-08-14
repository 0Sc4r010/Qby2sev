import argparse
from datetime import datetime
from Vista.business_rationale import insertar_encabezado_fc
from Vista.create_client import procesar_customer_data
from modelos.data_access import MSSQLConnectionManager, view_invoice_customer_data, view_invoice_data_head,process_view,clean_data
from modelos.api_total import process_api
import logging

# logging.basicConfig(level=logging.INFO,
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("app.log"),
                        logging.StreamHandler()
                    ])
logger = logging.getLogger(__name__)

proceso_global = ''
fecha_especifica = datetime(2025, 8, 13, 0, 0, 0)


def process_customer_data(proceso):
    try:
        customer_data = view_invoice_customer_data(proceso)
        if isinstance(customer_data, list) and customer_data:
            response_ = procesar_customer_data(customer_data)
    except Exception as e:
        print(f"An error occurred while processing customer data: {e}")


def invoicing_process(proceso_global):
    """
    The function `invoicing_process` processes invoice data by inserting header information based on
    payment method.
    else insert header inventory and accounting
    """
    try:
        invoice_data = view_invoice_data_head(proceso_global,'H')
        if isinstance(invoice_data, list) and invoice_data:
            for row in invoice_data:
                   insertar_encabezado_fc(row,proceso_global)
             
    except Exception as e:
        print(f"An error occurred while processing invoice data: {e}")


         

def main():
    """
    The `main` function in this Python script parses command line arguments, processes data based on the
    specified process type, and handles exceptions.
    """
    parser = argparse.ArgumentParser(description='Integracion Estaciones, Tiquetes a seven')
    # Agregar argumentos
    parser.add_argument('--proceso', type=str, default='T',help='Nombre del proceso [T]iquetes [R] Reproceso')
    
    # Parsear los argumentos
    args = parser.parse_args()
    proceso_global = args.proceso

    try:
            # proceso encargado de leer la vista (temporal) y cargar el repositorio de datos de tiquetes
            if  proceso_global == 'T' :
                clean_data(proceso_global)
                process_api(fecha_especifica)   # process_api(datetime.now()) 
                process_view(fecha_especifica)
                
            process_customer_data(proceso_global) 
            invoicing_process(proceso_global) # procesa Movimientos
           
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
    MSSQLConnectionManager.close_connection()    
  
  
if __name__ == "__main__":
    main()
