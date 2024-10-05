# Salary Report Generator

## Descripción
Salary Report Generator es una herramienta de Python diseñada para automatizar la creación de informes de salarios utilizando Google Sheets. Este script genera datos de muestra de empleados, los procesa y crea un informe detallado en una hoja de cálculo de Google, facilitando la gestión y análisis de información salarial.

## Características
- Generación de datos de empleados de muestra.
- Creación automática de una hoja de cálculo en Google Sheets.
- Cálculo de salario anual y años de servicio para cada empleado.
- Escritura de datos procesados en Google Sheets.
- Compartir automáticamente la hoja de cálculo con un correo electrónico especificado.

## Requisitos previos
- Python 3.6 o superior
- Cuenta de Google con acceso a Google Sheets
- Credenciales de API de Google (archivo `credentials.json`)

## Instalación

1. Clona este repositorio:
   ```
   git clone https://github.com/tu-usuario/salary-report-generator.git
   cd salary-report-generator
   ```

2. Instala las dependencias necesarias:
   ```
   pip install -r requirements.txt
   ```

3. Configura tus credenciales de Google API:
   - Sigue las [instrucciones de Google](https://developers.google.com/sheets/api/quickstart/python) para obtener un archivo `credentials.json`.
   - Coloca el archivo `credentials.json` en el directorio raíz del proyecto.

## Uso

1. Abre el archivo `main.py` y ajusta la variable `correo_personal` con tu dirección de correo electrónico.

2. Ejecuta el script:
   ```
   python main.py
   ```

3. El script generará datos de muestra, creará una hoja de cálculo en Google Sheets, procesará los datos y los escribirá en la hoja.

4. Al finalizar, recibirás un enlace para acceder a la hoja de cálculo creada.

## Personalización

- Para modificar el número de empleados generados, ajusta el argumento en la función `generar_datos_empleados()` dentro de `main()`.
- Puedes personalizar los rangos de salarios y fechas de contratación en la función `generar_datos_empleados()`.

## Contribuir

Las contribuciones son bienvenidas. Por favor, abre un issue para discutir cambios mayores antes de crear un pull request.

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Contacto

Si tienes preguntas o sugerencias, por favor abre un issue en este repositorio.

---

Desarrollado por Héctor M. Ruiz-Juárez
