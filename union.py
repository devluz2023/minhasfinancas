import os

def exportar_projeto(arquivo_saida="projeto_completo.txt", diretorio_raiz="."):
    """
    Lê todos os arquivos relevantes do projeto e une em um único txt.
    Ignora pastas de sistema, ambientes virtuais e arquivos sensíveis.
    """
    
    # Pastas que o script não deve tentar ler
    pastas_ignoradas = {
        '.git', '.venv', 'venv', 'env', '__pycache__', 
        '.pytest_cache', '.terraform', 'node_modules'
    }
    
    # Arquivos que devem ser ignorados por segurança ou redundância
    arquivos_ignorados = {
        '.env',                 # NUNCA expor chaves de API
        arquivo_saida,          # Evita que o script leia o próprio arquivo que está criando
        '.DS_Store'             # Arquivo de sistema do macOS
    }
    
    # Extensões ou nomes exatos permitidos
    extensores_permitidos = {'.py', '.txt', '.md', '.tf', '.gitignore'}
    arquivos_sem_extensao_permitidos = {'Dockerfile'}

    arquivos_lidos = 0

    print(f"Gerando arquivo: {arquivo_saida} ...\n")
    
    with open(arquivo_saida, 'w', encoding='utf-8') as f_saida:
        for root, dirs, files in os.walk(diretorio_raiz):
            # Remove as pastas ignoradas da busca in-place
            dirs[:] = [d for d in dirs if d not in pastas_ignoradas]
            
            for file in files:
                if file in arquivos_ignorados:
                    continue
                
                _, ext = os.path.splitext(file)
                
                # Verifica se o arquivo é válido para leitura
                if ext in extensores_permitidos or file in arquivos_sem_extensao_permitidos:
                    caminho_completo = os.path.join(root, file)
                    
                    try:
                        with open(caminho_completo, 'r', encoding='utf-8') as f_entrada:
                            conteudo = f_entrada.read()
                            
                            # Formata o cabeçalho de cada arquivo no txt
                            f_saida.write("=" * 60 + "\n")
                            f_saida.write(f"ARQUIVO: {caminho_completo}\n")
                            f_saida.write("=" * 60 + "\n\n")
                            f_saida.write(conteudo)
                            f_saida.write("\n\n")
                            
                            arquivos_lidos += 1
                            print(f"Adicionado: {caminho_completo}")
                    except Exception as e:
                        print(f"⚠️ Erro ao ler {caminho_completo}: {e}")

    print(f"\n✅ Concluído! {arquivos_lidos} arquivos foram unidos em '{arquivo_saida}'.")

if __name__ == "__main__":
    exportar_projeto()