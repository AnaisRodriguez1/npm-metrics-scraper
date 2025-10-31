import scrapy
import requests
import tarfile
import os
import shutil
from io import BytesIO
import esprima

class LocalCodeAnalysisPipeline:

    def count_functions_in_ast(self, tree):
        count = 0

        def visit_nodes(node, parent_type=None):
            nonlocal count

            if not hasattr(node, 'type'):
                return

            node_type = getattr(node, 'type', None)
            
            # Contar funciones, pero evitar doble conteo de FunctionExpression dentro de MethodDefinition
            if node_type == 'FunctionDeclaration':
                count += 1
            elif node_type == 'ArrowFunctionExpression':
                count += 1
            elif node_type == 'MethodDefinition':
                count += 1
                # NO contar el FunctionExpression interno del método
            elif node_type == 'FunctionExpression':
                # Solo contar si NO es parte de un MethodDefinition
                if parent_type != 'MethodDefinition':
                    count += 1

            # Visitar nodos hijos
            for key, value in vars(node).items():
                if hasattr(value, 'type'):
                    visit_nodes(value, node_type)
                elif isinstance(value, list):
                    for item in value:
                        if hasattr(item, 'type'):
                            visit_nodes(item, node_type)
        
        if tree:
            visit_nodes(tree)
        return count


    def process_item(self, item, spider):
        tarball_size_bytes = item.get('tarball_size_bytes')
        
        # 1. Only proceed if the tarball URL exists
        if item.get('tarball_url'):
            package_name = item['package_name']
            tarball_url = item['tarball_url']
            temp_dir = f'./temp_{package_name}'

            try:
                # 1. Download the .tgz file
                spider.logger.info(f"Downloading tarball for {package_name} from {tarball_url}")
                headers = {'User-Agent': spider.settings.get('USER_AGENT')}
                response = requests.get(tarball_url, stream=True, headers=headers)
                response.raise_for_status() 
                
                # 2. Decompression and Analysis Setup
                with tarfile.open(fileobj=BytesIO(response.content), mode="r:gz") as tar:
                    tar.extractall(path=temp_dir)
                    
                    total_files = 0
                    total_functions = 0 

                    for root, _, files in os.walk(temp_dir):
                        for file_name in files:
                            if file_name.endswith(('.js', '.ts', '.jsx', '.tsx')):
                                file_path = os.path.join(root, file_name)
                                total_files += 1  # Contar TODOS los archivos antes de parsear
                                
                                try:
                                    with open(file_path, 'r', encoding='utf-8') as f:
                                        code = f.read()
                                    
                                    ast_tree = None
                                    try:
                                        ast_tree = esprima.parseModule(code, options={'tolerant': True})
                                    except:
                                        try:
                                            ast_tree = esprima.parseScript(code, options={'tolerant': True})
                                        except:
                                            pass
                                    
                                    if ast_tree:
                                        # Count functions using my helper function
                                        file_functions = self.count_functions_in_ast(ast_tree)
                                        total_functions += file_functions
                                    
                                except Exception as e:
                                    spider.logger.warning(f"Unexpected Error during AST analysis of {file_name}: {e}")
                                
                    # 3. Store Results (from the real AST analysis)
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
                # 4. Cleanup: Remove the temporary directory to save space
                if os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir)
                    
        # FINAL DATA CLEANUP (Always executes, even if download failed)
        if 'tarball_url' in item:
            del item['tarball_url']
            
        return item