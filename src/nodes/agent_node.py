from langchain_core.messages import SystemMessage

from src.state import AgentState
from src.llm import get_llm
from src.prompts.system_prompts import AGENT_SYSTEM_PROMPT
from src.tools.web_search import search_web
from src.tools.database import consultar_status_pedido
# 1. Importe a nova ferramenta de RAG que criamos
from src.tools.rag_retriever import buscar_documentos_internos
from src.tools.yahoo_finance import buscar_dados_yahoo_finance

# 2. Adicione a ferramenta de RAG na lista de ferramentas disponíveis
tools = [search_web, consultar_status_pedido, buscar_documentos_internos, buscar_dados_yahoo_finance]

# Inicializa o LLM e vincula as ferramentas
llm = get_llm()
llm_with_tools = llm.bind_tools(tools)

def agent_node(state: AgentState):
    """
    Nó principal de raciocínio.
    Lê o histórico, injeta o prompt do sistema e decide o próximo passo.
    """
    # Injeta o prompt do sistema no início das mensagens
    messages = [SystemMessage(content=AGENT_SYSTEM_PROMPT)] + state["messages"]
    
    # Invoca o modelo
    response = llm_with_tools.invoke(messages)
    
    # Atualiza o estado
    return {"messages": [response]}