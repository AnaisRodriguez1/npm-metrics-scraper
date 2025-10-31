# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NpmMetricsPackageItem(scrapy.Item):
    # Key field
    package_name = scrapy.Field()
    
    # NPM public URL
    public_url = scrapy.Field()
    
    # DShort description/purpose of the package
    purpose = scrapy.Field()
    
    #  Step B Downloads API
    downloads_last_month = scrapy.Field()
    
    # Step C Registry API
    dependencies = scrapy.Field()
    version = scrapy.Field()
    size_mb = scrapy.Field()  # Package size in MB (unpacked)
    
    # Tarball URL (for internal use in Pipeline only)
    tarball_url = scrapy.Field()
    
    #Local Analysis Metrics (from Step D - Pipeline)
    total_files = scrapy.Field()
    total_functions = scrapy.Field()

    #New additional metrics
    license = scrapy.Field()
    maintainer_count = scrapy.Field()
    last_modified = scrapy.Field()
