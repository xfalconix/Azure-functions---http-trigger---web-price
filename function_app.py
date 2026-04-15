import azure.functions as func
import logging
import requests
import datetime

# Nota: el nombre del archivo debe ser function_app.py, de lo contrario no se ejecutará la función.

# Creamos la aplicación de Azure Functions con acceso anónimo (sin autenticación)
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="http_trigger_precios_web")
def http_trigger_precios_web(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Función HTTP disparada: consultando precio del producto.')

    # --- 1. URL del producto a consultar ---
    # Leemos la URL desde los parámetros de la petición HTTP (?url=...)
    # Si no se proporciona, usamos la URL de ejemplo del notebook
    url = req.params.get('url') or 'https://www.aftgrupo.com/productos/ref-14062510'

    # --- 2. Descargar el HTML de la página ---
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Lanza un error si el servidor devuelve 4xx o 5xx
        html_content = response.text
    except requests.exceptions.RequestException as e:
        # Si falla la conexión, devolvemos un error 502 con el mensaje
        logging.error(f"Error al obtener la página: {e}")
        return func.HttpResponse(f"Error al obtener la página: {e}", status_code=502)

    # --- 3. Extraer el nombre del producto del HTML ---
    product_name = 'No encontrado'
    start_name_tag = '<strong>DESCRIPCIÓN:</strong><br>'
    end_name_tag = '<br />'
    name_start_idx = html_content.find(start_name_tag)
    if name_start_idx != -1:
        name_start_idx += len(start_name_tag)
        name_end_idx = html_content.find(end_name_tag, name_start_idx)
        if name_end_idx != -1:
            product_name = html_content[name_start_idx:name_end_idx].strip().replace('\r\n', '')

    # --- 4. Extraer el precio del producto del HTML ---
    product_price = 'No encontrado'
    start_price_tag = '<div class="precio_ficha">'
    end_price_tag = '</div>'
    price_start_idx = html_content.find(start_price_tag)
    if price_start_idx != -1:
        price_start_idx += len(start_price_tag)
        price_end_idx = html_content.find(end_price_tag, price_start_idx)
        if price_end_idx != -1:
            product_price = html_content[price_start_idx:price_end_idx].strip()

    # --- 5. Registrar y devolver el resultado ---
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    resultado = (
        f"Producto:   {product_name}\n"
        f"Precio:     {product_price}\n"
        f"Timestamp:  {timestamp}\n"
        f"URL:        {url}"
    )
    logging.info(resultado)

    return func.HttpResponse(resultado, status_code=200)
