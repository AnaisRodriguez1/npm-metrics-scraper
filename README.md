# 📊 NPM Metrics Scraper

Herramienta de análisis automatizado para extraer métricas de paquetes NPM mediante web scraping. Combina APIs públicas de NPM con análisis estático de código (AST) para obtener información completa sobre paquetes JavaScript/TypeScript.

## Flujo de Trabajo

### **PASO A: Descubrimiento**
El spider comienza con una lista de paquetes (por ejemplo: `react`, `axios`, `lodash`).

```python
package_list = ['react', 'axios', 'lodash']
```

### **PASO B: API de Descargas**
Para cada paquete, consulta la API de NPM para obtener las **descargas del último mes**.

```
https://api.npmjs.org/downloads/point/last-month/react
```

### **PASO C: API de Registro (Metadata)**
Luego consulta la Registry API de NPM para obtener información detallada:

```
https://registry.npmjs.org/react
```

**Datos que obtiene:**
- ✅ Versión actual (`version`)
- ✅ Descripción/propósito (`purpose`)
- ✅ Dependencias (`dependencies`)
- ✅ Tamaño descomprimido (`size_mb`)
- ✅ Licencia (`license`)
- ✅ Autor del paquete (`author`)
- ✅ Número de mantenedores (`maintainer_count`)
- ✅ Última modificación (`last_modified`)
- ✅ URL del tarball (para descarga)
- ✅ URL pública del paquete

### **PASO D: Análisis Local de Código**
El Pipeline descarga el archivo `.tgz` del paquete y analiza:

1. **Descarga el tarball** (archivo comprimido del paquete)
2. **Descomprime** en una carpeta temporal
3. **Cuenta archivos** JavaScript/TypeScript (`.js`, `.ts`, `.jsx`, `.tsx`)
4. **Analiza el código fuente con AST** usando [esprima](https://esprima.org/):
   - Parsea cada archivo JS/TS generando un árbol de sintaxis abstracta (AST)
   - Recorre el AST detectando funciones: `FunctionDeclaration`, `ArrowFunctionExpression`, `MethodDefinition`, `FunctionExpression`
   - Evita doble conteo de funciones internas en métodos
5. **Limpia** la carpeta temporal

## Datos Capturados

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
| `author` | Autor del paquete | `"Meta"` |
| `maintainer_count` | Número de mantenedores |
| `last_modified` | Fecha de última modificación |
| `total_files` | Archivos JS/TS/JSX/TSX en el paquete |
| `total_functions` | Funciones detectadas con AST |
| `tarball_url` | URL del archivo comprimido |

## Instalación

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

## Uso

### Ejecutar el Scraper

```bash
cd npm-metrics-package
scrapy crawl package_info_spider -o npm_metrics_results.json
```

### Cambiar los Paquetes a Analizar

Para cambiar los paquetes, se debe editar el archivo `npm_metrics_package/spiders/package_info_spider.py`:

```python
package_list = ['react', 'vue', 'angular', 'express', 'next']
```

### Ver los Resultados

Los resultados se guardan en `npm_metrics_results.json`.

### Ejecutar Tests

Para verificar que el contador de funciones AST funciona correctamente:

```bash
cd npm-metrics-package
python test_ast_counter.py
```

El test valida que la función `count_functions_in_ast()` detecte correctamente:
- Function declarations
- Arrow functions
- Class methods
- Mixed function types
- Nested functions

## Configuración

### Ajustar la Velocidad del Scraping

En `npm_metrics_package/settings.py`:

```python
# Espera 1 segundo entre cada request (evita saturar el servidor)
DOWNLOAD_DELAY = 1

# Solo 1 request simultáneo por dominio
CONCURRENT_REQUESTS_PER_DOMAIN = 1
```

### Cambiar el User-Agent

En `npm_metrics_package/settings.py`, personaliza el User-Agent con su correo electrónico:

```python
USER_AGENT = 'npm_metrics_package (tu-email@ejemplo.com)'
```

## Tecnologías Utilizadas

- **[Scrapy 2.13](https://scrapy.org/)** - Framework de web scraping
- **[Python 3.11](https://www.python.org/)** - Lenguaje de programación
- **[Esprima](https://esprima.org/)** - Parser de JavaScript para análisis AST
- **[Requests](https://requests.readthedocs.io/)** - Cliente HTTP para descargar tarballs
- **APIs de NPM:**
  - Downloads API: `api.npmjs.org`
  - Registry API: `registry.npmjs.org`

## Arquitectura del Proyecto

```
npm-metrics-scraper/
├── npm-metrics-package/
│   ├── npm_metrics_package/
│   │   ├── spiders/
│   │   │   └── package_info_spider.py    # Spider principal
│   │   ├── items.py                       # Definición de datos
│   │   ├── pipelines.py                   # Procesamiento y análisis AST
│   │   ├── settings.py                    # Configuración
│   │   └── middlewares.py
│   ├── scrapy.cfg
│   ├── requirements.txt
│   └── npm_metrics_results.json           # Resultados
└── README.md
```