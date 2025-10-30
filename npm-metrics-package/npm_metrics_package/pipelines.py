import scrapy
import requests
import tarfile
import os
import shutil
from io import BytesIO

class LocalCodeAnalysisPipeline:
    def process_item(self, item, spider):
        # Only process if we have the tarball URL
        if item.get('tarball_url'):
            package_name = item['package_name']
            tarball_url = item['tarball_url']
            temp_dir = f'./temp_{package_name}'

            try:
                # 1. Download the .tgz
                spider.logger.info(f"Downloading tarball for {package_name} from {tarball_url}")
                # Use a good User-Agent for requests too
                headers = {'User-Agent': spider.settings.get('USER_AGENT')}
                response = requests.get(tarball_url, stream=True, headers=headers)
                response.raise_for_status() # Raise error for bad HTTP codes
                
                # 2. Decompression and Analysis
                with tarfile.open(fileobj=BytesIO(response.content), mode="r:gz") as tar:
                    tar.extractall(path=temp_dir)
                    
                    # --- Analysis Logic (Mock/Simulation) ---
                    total_files = 0
                    total_functions = 0 # Simulation

                    for root, _, files in os.walk(temp_dir):
                        for file_name in files:
                            # Count JS/TS files
                            if file_name.endswith(('.js', '.ts', '.jsx', '.tsx')):
                                total_files += 1
                                # Real implementation would use an AST parser here 
                                # (e.g., slimit, javascripthon) to count functions.
                                
                                # Current simulation for illustrative purposes:
                                if total_files % 2 == 0:
                                    total_functions += 5 
                                else:
                                    total_functions += 2
                                
                    # 3. Store Results
                    item['total_files'] = total_files
                    item['total_functions'] = total_functions
                    spider.logger.info(f"Local Analysis: {total_files} files, {total_functions} functions for {package_name}")
                    
            except requests.exceptions.RequestException as e:
                spider.logger.error(f"Tarball download error for {package_name}: {e}")
            except tarfile.TarError as e:
                spider.logger.error(f"Decompression error for {package_name}: {e}")
            except Exception as e:
                spider.logger.error(f"Unexpected error during analysis for {package_name}: {e}")
            finally:
                # 4. Cleanup: Remove the temporary directory
                if os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir)
                    
        return item