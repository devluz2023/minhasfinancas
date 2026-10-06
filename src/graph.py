from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import SystemMessage, AIMessage # CORREÇÃO 1: Importado AIMessage

# Importações dos módulos do nosso projeto
from src.state import AgentState
from src.llm import get_llm
from src.prompts.system_prompts import AGENT_SYSTEM_PROMPT

# Importação das Ferramentas (Incluindo RAG e Yahoo Finance)
from src.tools.web_search import search_web
from src.tools.database import consultar_status_pedido
from src.tools.rag_retriever import buscar_documentos_internos
from src.tools.yahoo_finance import buscar_dados_yahoo_finance

# Importação do Guardrail que criamos na pasta nodes
from src.nodes.guardrail_node import guardrail_node # CORREÇÃO 2: Importado Guardrail

# ==========================================
# 1. Ferramentas (Tools)
# ==========================================
tools = [
    search_web, 
    consultar_status_pedido, 
    buscar_documentos_internos, 
    buscar_dados_yahoo_finance
]

# ==========================================
# 2. Configuração do Agente e Roteador
# ==========================================
llm = get_llm()
llm_with_tools = llm.bind_tools(tools)

def roteador_pos_guardrail(state: AgentState):
    """Verifica se o Guardrail gerou uma mensagem de bloqueio."""
    ultima_mensagem = state["messages"][-1]
    
    # Se a última mensagem for da IA e contiver nosso aviso de Guardrail, encerramos.
    if isinstance(ultima_mensagem, AIMessage) and "🛡️ **Guardrail Ativado:**" in ultima_mensagem.content:
        return END
    
    # Caso contrário, está limpo. Passa para o agente principal.
    return "agent"

def agent_node(state: AgentState):
    """Nó principal que invoca o modelo de linguagem."""
    # Injeta o prompt do sistema como a primeira mensagem
    messages = [SystemMessage(content=AGENT_SYSTEM_PROMPT)] + state["messages"]
    
    # O modelo analisa o prompt, o histórico e decide se usa uma ferramenta ou responde
    response = llm_with_tools.invoke(messages)
    
    # Atualiza o estado anexando a resposta
    return {"messages": [response]}

# ==========================================
# 3. Construção do Grafo (StateGraph)
# ==========================================
workflow = StateGraph(AgentState)

# Adiciona os nós (Paradas do grafo)
workflow.add_node("guardrail", guardrail_node) # CORREÇÃO 4: Adicionado nó do guardrail
workflow.add_node("agent", agent_node)
workflow.add_node("tools", ToolNode(tools))

# Define o fluxo (Edges)
workflow.add_edge(START, "guardrail") # CORREÇÃO 3: O fluxo agora começa no guardrail!

# O roteador decide se vai para o agente ou se encerra (caso bloqueado)
workflow.add_conditional_edges(
    "guardrail",
    roteador_pos_guardrail
)

# Aresta condicional do agente para as ferramentas
workflow.add_conditional_edges(
    "agent",
    tools_condition,
)

# Após a ferramenta rodar, o fluxo DEVE voltar para o agente
workflow.add_edge("tools", "agent")

# Compila o aplicativo para ser importado no main.py
app = workflow.compile()