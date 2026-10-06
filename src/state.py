from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage

class AgentState(TypedDict):
    # O reducer 'add_messages' garante que novas mensagens sejam anexadas
    # à lista existente em vez de substituí-la.
    messages: Annotated[list[AnyMessage], add_messages]
    
    # Exemplo de outras chaves de estado que você pode adicionar no futuro:
    # usuario_logado: str
    # passos_executados: int