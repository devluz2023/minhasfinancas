from langchain_core.messages import AIMessage
from src.state import AgentState

def human_node(state: AgentState):
    """
    Nó de aprovação humana (Human-in-the-loop).
    É acionado quando o agente precisa de confirmação antes de uma ação crítica.
    """
    # No futuro, o LangGraph pausará a execução antes de entrar aqui.
    # Por enquanto, ele apenas adiciona uma mensagem informando que passou por aprovação.
    
    mensagem_aprovacao = AIMessage(
        content="[Revisão Humana Concluída] O usuário autorizou a continuação desta ação."
    )
    
    return {"messages": [mensagem_aprovacao]}