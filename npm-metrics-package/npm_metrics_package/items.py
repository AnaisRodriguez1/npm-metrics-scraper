# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NpmMetricsPackageItem(scrapy.Item):
    # Campo clave
    package_name = scrapy.Field()
    
    # URL de la página pública de NPM
    public_url = scrapy.Field()
    
    # Descripción corta/propósito del paquete
    purpose = scrapy.Field()
    
    # Métrica de Descargas (del Paso B - API Downloads)
    downloads_last_month = scrapy.Field()
    
    # Métricas de Metadatos (del Paso C - Registry API)
    dependencies = scrapy.Field()
    version = scrapy.Field()
    tarball_size_bytes = scrapy.Field()
    
    # URL del tarball (solo para uso interno en el Pipeline)
    tarball_url = scrapy.Field()
    
    # Métricas de Análisis Local (del Paso D - Pipeline)
    total_files = scrapy.Field()
    total_functions = scrapy.Field()
