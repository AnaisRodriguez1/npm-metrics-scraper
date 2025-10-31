# 📊 NPM Metrics Scraper

## Arquitectura del Proyecto

```
npm-metrics-scraper/
├── npm-metrics-package/          # Carpeta principal del proyecto Scrapy
│   ├── npm_metrics_package/      # Paquete Python con el código
│   │   ├── spiders/              # 🕷️ Los "robots" que hacen el scraping
│   │   │   └── package_info_spider.py  # Spider principal
│   │   ├── items.py              # 📋 Define qué datos queremos capturar
│   │   ├── pipelines.py          # 🔧 Procesa los datos descargados
│   │   ├── settings.py           # ⚙️ Configuración del scraper
│   │   └── middlewares.py        # 🔌 Middleware (no usado actualmente)
│   ├── scrapy.cfg                # Configuración de Scrapy
│   ├── requirements.txt          # Dependencias del proyecto
│   └── npm_metrics_results.json  # 💾 Resultados generados
└── README.md                     # 📖 Este archivo
```

## Flujo de Trabajo

### **PASO A: Descubrimiento** 🔍
El spider comienza con una lista de paquetes (por ejemplo: `react`, `axios`, `lodash`).

```python
package_list = ['react', 'axios', 'lodash']
```

### **PASO B: API de Descargas** 📊
Para cada paquete, consulta la API de NPM para obtener las **descargas del último mes**.

```
📡 https://api.npmjs.org/downloads/point/last-month/react
```

### **PASO C: API de Registro (Metadata)** 📝
Luego consulta la Registry API de NPM para obtener información detallada:

```
📡 https://registry.npmjs.org/react
```

**Datos que obtiene:**
- ✅ Versión actual (`version`)
- ✅ Descripción/propósito (`purpose`)
- ✅ Dependencias (`dependencies`)
- ✅ Tamaño descomprimido (`size_mb`)
- ✅ Licencia (`license`)
- ✅ Número de mantenedores (`maintainer_count`)
- ✅ Última modificación (`last_modified`)
- ✅ URL del tarball (para descarga)
- ✅ URL pública del paquete

### **PASO D: Análisis Local de Código** 🔬
El Pipeline descarga el archivo `.tgz` del paquete y analiza:

1. **Descarga el tarball** (archivo comprimido del paquete)
2. **Descomprime** en una carpeta temporal
3. **Cuenta archivos** JavaScript/TypeScript (`.js`, `.ts`, `.jsx`, `.tsx`)
4. **Simula conteo de funciones** (AST implementado)
5. **Limpia** la carpeta temporal

## 📋 Datos Capturados

Para cada paquete NPM, el scraper recopila:

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| `package_name` | Nombre del paquete | `"react"` |
| `public_url` | URL pública en npmjs.com | `"https://www.npmjs.com/package/react"` |
| `purpose` | Descripción corta | `"React is a JavaScript library..."` |
| `downloads_last_month` | Descargas del último mes | 
| `version` | Versión actual |
| `size_mb` | Tamaño descomprimido en MB |
| `dependencies` | Dependencias del paquete | `{}` o `{"lodash": "^4.17.0"}` |
| `license` | Tipo de licencia |
| `maintainer_count` | Número de mantenedores |
| `last_modified` | Fecha de última modificación |
| `total_files` | Archivos JS/TS en el paquete |
| `total_functions` | Funciones detectadas (simulado) |
| `tarball_url` | URL del archivo comprimido |

## 🚀 Instalación

### Requisitos Previos
- Python 3.11 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/AnaisRodriguez1/npm-metrics-scraper.git
cd npm-metrics-scraper
```

2. **Crear entorno virtual** (recomendado)
```bash
python -m venv .venv
```

3. **Activar el entorno virtual**

En Windows (PowerShell):
```powershell
.venv\Scripts\Activate.ps1
```

En Windows (CMD):
```cmd
.venv\Scripts\activate.bat
```

En Linux/Mac:
```bash
source .venv/bin/activate
```

4. **Instalar dependencias**
```bash
cd npm-metrics-package
pip install -r requirements.txt
```

## 💻 Uso

### Ejecutar el Scraper

```bash
cd npm-metrics-package
scrapy crawl package_info_spider -o npm_metrics_results.json
```

### Cambiar los Paquetes a Analizar

Edita el archivo `npm_metrics_package/spiders/package_info_spider.py`:

```python
package_list = ['react', 'vue', 'angular', 'express', 'next']
```

### Ver los Resultados

Los resultados se guardan en `npm_metrics_results.json`:

## ⚙️ Configuración

### Ajustar la Velocidad del Scraping

En `npm_metrics_package/settings.py`:

```python
# Espera 1 segundo entre cada request (evita saturar el servidor)
DOWNLOAD_DELAY = 1

# Solo 1 request simultáneo por dominio
CONCURRENT_REQUESTS_PER_DOMAIN = 1
```

### Cambiar el User-Agent

```python
USER_AGENT = 'npm_metrics_package (tu-email@ejemplo.com)'
```

## 🛠️ Tecnologías Utilizadas

- **[Scrapy 2.13](https://scrapy.org/)** - Framework de web scraping
- **[Python 3.11](https://www.python.org/)** - Lenguaje de programación
- **[Requests](https://requests.readthedocs.io/)** - Para descargar tarballs
- **APIs de NPM:**
  - Downloads API: `api.npmjs.org`
  - Registry API: `registry.npmjs.org`