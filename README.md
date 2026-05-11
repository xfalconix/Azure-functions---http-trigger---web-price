# 🌐 Azure Price Scraper — HTTP Trigger

<a href="https://azure.microsoft.com/services/functions"><img src="https://img.shields.io/badge/Azure%20Functions-0062AD?style=flat-square&logo=microsoftazure&logoColor=white" alt="Azure Functions"/></a>
<a href="https://pypi.org/project/requests/"><img src="https://img.shields.io/badge/requests-FF6849?style=flat-square&logo=python&logoColor=white" alt="requests"/></a>
<a href="https://github.com/xfalconix/azure-price-scraper/actions"><img src="https://github.com/xfalconix/azure-price-scraper/actions/workflows/main_httptriggerpriceweb.yml/badge.svg" alt="CI"/></a>

Azure Function con **HTTP Trigger** que hace web scraping de precios de productos: extrae nombre y precio de cualquier página web y devuelve la información en texto plano con timestamp.

---

## 🎯 Objetivo

Automatizar la monitorización de precios de productos en la web. Ideal para:
- Alerts de precio para compras recurrentes
-Seguimiento de competidores o proveedores
- Pipeline de datos para analytics de pricing

---

## ⚡ Arquitectura

```
Petición HTTP (GET)
       │
       ▼
Azure Functions — HTTP Trigger
       │
       ▼
requests.get(URL)  →  BeautifulSoup / parsing HTML
       │
       ▼
Respuesta: nombre + precio + timestamp
```

---

## 🛠 Stack Tecnológico

| Componente | Tecnología |
|-----------|------------|
| Serverless | Azure Functions (Python) |
| HTTP Client | `requests` |
| CI/CD | GitHub Actions |
| Runtime | Python 3.11+ |

---

## 📡 Uso de la API

### Endpoint

```
GET https://<your-function-app>.azurewebsites.net/api/http_trigger_precios_web
```

### Parámetros

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `url` | query string | URL del producto a consultar (opcional, usa默认值 si no se provee) |

### Ejemplo de respuesta

```
Producto:   Válvula de bola DN50 3-piece SS316
Precio:     89,50 €
Timestamp:  2026-04-15 10:32:01
URL:        https://www.aftgrupo.com/productos/ref-14062510
```

### Ejemplo de llamada

```bash
curl "https://<your-function-app>.azurewebsites.net/api/http_trigger_precios_web?url=https://www.aftgrupo.com/productos/ref-14062510"
```

---

## 📁 Estructura del proyecto

```
.
├── function_app.py              # Azure Function con HTTP trigger
├── host.json                    # Configuración de Azure Functions runtime
├── requirements.txt             # Dependencias Python
├── .funcignore                  # Archivos excluidos del despliegue
├── .github/workflows/           # GitHub Actions CI/CD
│   └── main_httptriggerpriceweb.yml
└── README.md
```

---

## 🚀 Despliegue

### Requisitos previos

- Cuenta de Azure con Functions habilitado
- Azure CLI instalado (`az login`)
- Azure Functions Core Tools

### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/xfalconix/azure-price-scraper.git
cd azure-price-scraper

# 2. Crear Function App en Azure
az functionapp create \
  --resource-group <tu-rg> \
  --name <tu-function-app> \
  --storage-account <tu-storage> \
  --consumption-plan-location westeurope \
  --runtime python \
  --runtime-version 3.11

# 3. Desplegar
func azure functionapp publish <tu-function-app>
```

---

## 📊 Desarrollo local

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar localmente
func start

# Probar
curl "http://localhost:7071/api/http_trigger_precios_web?url=https://www.ejemplo.com/producto"
```

---

## 🔧 Personalización

Para apuntar a una web diferente, modifica los tags HTML en `function_app.py`:

```python
start_name_tag = '<strong>DESCRIPCIÓN:</strong><br>'
start_price_tag = '<div class="precio_ficha">'
```

Inspecciona el HTML del sitio destino con DevTools (F12) para ajustar los selectores.

---

## 📌 Mejoras futuras

- [ ] Extracción de múltiples productos en una sola llamada
- [ ] Almacenamiento de histórico en Azure Cosmos DB o Blob Storage
- [ ] Alert system por email o Telegram cuando el precio baje
- [ ] Despliegue con Terraform + infraestructura como código
- [ ] Tests con Playwright para validar extracción en sitios dinámicos (JS-rendered)

---

## 👤 Autor

Carlos Falconi — Project Engineer transicionando a Data & MLOps  
📍 ESESA Business School, Málaga — 2025-2026
