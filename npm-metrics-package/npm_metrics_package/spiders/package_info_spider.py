import scrapy
from npm_metrics_package.items import NpmMetricsPackageItem
import json

class PackageInfoSpider(scrapy.Spider):
    name = 'package_info_spider'
    allowed_domains = ['api.npmjs.org', 'registry.npmjs.org', 'npmjs.com']

    package_list = ['react','axios','lodash']

    # INICIO DEL FLUJO (STEP A : DISCOVERY)
    def start_requests(self):
        
        for package_name in self.package_list:
            item = NpmMetricsPackageItem(package_name=package_name)
            
            # Guardamos la URL pública del paquete
            item['public_url'] = f'https://www.npmjs.com/package/{package_name}'

            downloads_url = f'https://api.npmjs.org/downloads/point/last-month/{package_name}'

            yield scrapy.Request(
                url=downloads_url,
                callback=self.parse_downloads,
                meta= {'item': item}
            )

    #CALLBACK 1 (STEP B: API ORCHESTRATION - DOWNLOADS)
    def parse_downloads(self, response):
        item = response.meta['item']

        try:
            data = json.loads(response.text)
            item['downloads_last_month'] = data.get('downloads',0)
        except json.JSONDecodeError:
            self.logger.warning(f"Error decoding downloads for {item['package_name']}")
        

        registry_url = f'https://registry.npmjs.org/{item["package_name"]}'

        yield scrapy.Request(
            url=registry_url,
            callback=self.parse_registry_metadata,
            meta={'item': item}
        )
    
    #CALLBACK 2 (STEP C: METADATA AND SOURCE CODE - REGISTRY API)
    def parse_registry_metadata(self, response):
        item = response.meta['item']

        try:
            data = json.loads(response.text)
            
            # Extraemos el propósito (descripción del paquete)
            item['purpose'] = data.get('description', 'No description available')
            
            latest_version = data.get('dist-tags', {}).get('latest')

            if latest_version:
                version_data = data['versions'][latest_version]

                item['version'] = latest_version
                item['dependencies'] = version_data.get('dependencies', {})
                item['tarball_size_bytes'] = version_data.get('dist', {}).get('unpackedSize')
                item['tarball_url'] = version_data.get('dist', {}).get('tarball')
            return item
    
        except json.JSONDecodeError:
            self.logger.error(f"Error decoding registry metadata for {item['package_name']}")

        return item
