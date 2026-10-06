from langchain_openai import ChatOpenAI
from src.config import config

def get_llm():
    """
    Inicializa e retorna o modelo de linguagem padrão do projeto.
    """
    if not config.OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY não encontrada no arquivo .env")
        
    return ChatOpenAI(
        model=config.MODEL_NAME,
        temperature=config.TEMPERATURE,
        api_key=config.OPENAI_API_KEY
    )