from langchain_core.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
from src.config import config

# Verifica se a chave foi configurada no .env
if not config.TAVILY_API_KEY:
    print("Aviso: TAVILY_API_KEY não encontrada. A ferramenta de busca na web pode falhar.")

# Instancia a ferramenta do LangChain configurada para trazer os 3 melhores resultados
tavily_tool = TavilySearchResults(
    max_results=3,
    tavily_api_key=config.TAVILY_API_KEY
)

@tool
def search_web(query: str) -> str:
    """
    Realiza uma busca na internet para encontrar informações atualizadas.
    Use esta ferramenta quando o usuário perguntar sobre notícias recentes, 
    fatos atuais ou algo que você não saiba de memória.
    """
    try:
        # Executa a busca
        resultados = tavily_tool.invoke({"query": query})
        
        # Formata os resultados em um texto legível para o LLM interpretar
        resposta_formatada = "Resultados da busca:\n\n"
        for i, res in enumerate(resultados, 1):
            resposta_formatada += f"{i}. {res['content']}\n(Fonte: {res['url']})\n\n"
            
        return resposta_formatada
    except Exception as e:
        return f"Erro ao realizar a busca na web: {str(e)}"