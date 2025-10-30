import requests
from bs4 import BeautifulSoup

# Cabeçalho para simular um navegador real, evitando bloqueios
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# 1. FAZER A REQUISIÇÃO
print("Acessando o G1...")
try:
    # Acessa a URL do G1
    response = requests.get("https://g1.globo.com/", headers=headers)
    
    # Verifica se a requisição foi bem-sucedida (código 200)
    response.raise_for_status() 

    # 2. "PARSEAR" (Analisar) O HTML
    # Pega o conteúdo da página e o prepara para o BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # 3. ENCONTRAR AS MANCHETES
    # Esta é a parte principal.
    # Inspecionando o G1, descobrimos que muitas manchetes estão dentro
    # de um link <a> com a classe "feed-post-link".
    print("Buscando manchetes...")
    
    # Usamos o find_all para encontrar TODAS as ocorrências dessa classe
    lista_de_links = soup.find_all('a', class_='feed-post-link')
    
    # 4. SALVAR EM UM ARQUIVO
    # 'w' = modo de escrita (write), 'encoding='utf-8'' garante que acentos funcionem
    with open('manchetes_g1.txt', 'w', encoding='utf-8') as f:
        f.write("=== MANCHETES DO G1 ===\n\n")
        
        if not lista_de_links:
            # Caso o G1 mude o layout e o script não ache nada
            f.write("Nenhuma manchete encontrada com o seletor 'feed-post-link'. O site pode ter atualizado.\n")
        else:
            # Loop para percorrer cada link encontrado
            for link in lista_de_links:
                # O .text pega apenas o texto de dentro da tag, ignorando o HTML
                manchete = link.text.strip() # .strip() remove espaços em branco extras
                
                # Vamos escrever no arquivo apenas se a manchete tiver texto
                if manchete:
                    print(f"Encontrado: {manchete}")
                    f.write(f"- {manchete}\n")
    
    print("\nSucesso! As manchetes foram salvas em 'manchetes_g1.txt'")

except requests.exceptions.RequestException as e:
    # Se a requisição falhar (sem internet, site fora do ar, etc.)
    print(f"Erro ao acessar a página: {e}")
except Exception as e:
    # Para qualquer outro erro inesperado
    print(f"Ocorreu um erro inesperado: {e}")