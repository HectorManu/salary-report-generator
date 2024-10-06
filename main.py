# Generador de Informe de Salarios

## 1. Importar bibliotecas necesarias

import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from datetime import datetime
import random
from faker import Faker

## 2. Configurar autenticación de Google Sheets

def obtener_autenticacion_google():
    """
    Configura y retorna las credenciales para la API de Google.
    
    Returns:
        Credentials: Objeto de credenciales para autenticar con la API de Google.
    """
    ALCANCE = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive"
    ]
    credenciales = Credentials.from_service_account_file("credentials.json", scopes=ALCANCE)
    return credenciales

## 3. Operaciones de Google Sheets

def crear_hoja_google(nombre_hoja):
    """
    Crea una nueva hoja de cálculo en Google Sheets con dos hojas de trabajo.
    
    Args:
        nombre_hoja (str): Nombre de la nueva hoja de cálculo.
    
    Returns:
        tuple: ID de la hoja de cálculo creada y los objetos de las hojas de trabajo.
    """
    credenciales = obtener_autenticacion_google()
    cliente = gspread.authorize(credenciales)
    
    # Crear una nueva hoja de cálculo
    hoja_calculo = cliente.create(nombre_hoja)
    id_hoja = hoja_calculo.id
    
    # Renombrar la primera hoja a 'Datos Empleados'
    hoja_datos = hoja_calculo.get_worksheet(0)
    hoja_datos.update_title("Datos Empleados")
    
    # Crear una segunda hoja llamada 'Reporte de Salarios'
    hoja_reporte = hoja_calculo.add_worksheet(title="Reporte de Salarios", rows="100", cols="20")
    
    # Configurar permisos para que cualquiera con el enlace pueda ver
    hoja_calculo.share('', perm_type='anyone', role='reader')
    
    print(f"Hoja de cálculo creada con ID: {id_hoja}")
    return id_hoja, hoja_datos, hoja_reporte

def compartir_hoja_google(id_hoja, email):
    """
    Comparte la hoja de cálculo con un correo electrónico específico para edición.
    
    Args:
        id_hoja (str): ID de la hoja de cálculo a compartir.
        email (str): Dirección de correo electrónico con la que se compartirá.
    """
    credenciales = obtener_autenticacion_google()
    cliente = gspread.authorize(credenciales)
    hoja_calculo = cliente.open_by_key(id_hoja)
    hoja_calculo.share(email, perm_type='user', role='writer')
    print(f"Hoja de cálculo compartida con {email} para edición")

def escribir_en_google_sheets(df, hoja_trabajo):
    """
    Escribe un DataFrame en una hoja de trabajo de Google Sheets.
    
    Args:
        df (DataFrame): DataFrame de pandas a escribir.
        hoja_trabajo (Worksheet): Objeto de hoja de trabajo de gspread.
    """
    hoja_trabajo.clear()
    # Convertir todas las columnas a string para evitar problemas de serialización
    df_string = df.astype(str)
    hoja_trabajo.update([df_string.columns.values.tolist()] + df_string.values.tolist())
    print(f"Datos escritos en la hoja: {hoja_trabajo.title}")

## 4. Generación y procesamiento de datos

def generar_datos_empleados(num_empleados=10):
    """
    Genera datos de empleados de muestra.
    
    Args:
        num_empleados (int): Número de empleados a generar (por defecto 10).
    
    Returns:
        DataFrame: DataFrame de pandas con los datos de los empleados.
    """
    fake = Faker()
    datos_empleados = []
    
    for _ in range(num_empleados):
        nombre = fake.name()
        salario = round(random.uniform(2000, 8000), 2)
        fecha_contratacion = fake.date_between(start_date='-24y', end_date='today')
        
        datos_empleados.append({
            "Nombre": nombre,
            "Salario Mensual": salario,
            "Fecha de Contratación": fecha_contratacion.strftime('%Y-%m-%d')  # Convertir fecha a string
        })
    
    return pd.DataFrame(datos_empleados)

def procesar_datos_empleados(df):
    """
    Procesa los datos de los empleados, calculando salario anual y años en la empresa.
    
    Args:
        df (DataFrame): DataFrame de pandas con los datos originales de los empleados.
    
    Returns:
        DataFrame: DataFrame de pandas con los datos procesados.
    """
    df['Salario Mensual'] = pd.to_numeric(df['Salario Mensual'], errors='coerce')
    df['Fecha de Contratación'] = pd.to_datetime(df['Fecha de Contratación'])
    
    df['Salario Anual'] = df['Salario Mensual'] * 12
    
    fecha_actual = datetime.now()
    df['Años en la Empresa'] = ((fecha_actual - df['Fecha de Contratación']).dt.days / 365).round(2)
    
    # Redondear salarios a dos decimales
    df['Salario Mensual'] = df['Salario Mensual'].round(2)
    df['Salario Anual'] = df['Salario Anual'].round(2)
    
    return df[['Nombre', 'Salario Mensual', 'Salario Anual', 'Años en la Empresa']]

## 5. Ejecución principal

def main():
    """
    Función principal que ejecuta todo el proceso de generación y carga del informe de salarios.
    """
    # Generar datos de muestra
    df_empleados = generar_datos_empleados(10)
    
    # Crear y configurar la hoja de Google
    nombre_hoja = "Informe de Salarios"
    id_hoja, hoja_datos, hoja_reporte = crear_hoja_google(nombre_hoja)
    correo_personal = "hectormanujuarez1987@gmail.com"  # Reemplaza con tu correo
    compartir_hoja_google(id_hoja, correo_personal)
    
    # Escribir datos originales en la primera hoja
    escribir_en_google_sheets(df_empleados, hoja_datos)
    
    # Procesar datos y escribir en la segunda hoja
    df_procesado = procesar_datos_empleados(df_empleados)
    escribir_en_google_sheets(df_procesado, hoja_reporte)
    
    print(f"Proceso completado. La hoja de cálculo es accesible para cualquier persona con este enlace:")
    print(f"https://docs.google.com/spreadsheets/d/{id_hoja}")
    print("Nota: El enlace permite solo la visualización. Para editar, usa la cuenta con la que se compartió el documento.")

if __name__ == "__main__":
    main()