from langgraph.prebuilt import ToolNode

# Importamos a mesma lista de ferramentas usada no agent_node
from src.nodes.agent_node import tools

# Criamos a instância do nó de ferramentas do LangGraph.
# Isso executará automaticamente a ferramenta que o agente pedir.
tool_node = ToolNode(tools)