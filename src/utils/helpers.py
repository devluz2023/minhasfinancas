from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    ToolMessage,
    SystemMessage,
    AnyMessage
)

def format_message(message: AnyMessage) -> str:
    """
    Recebe um objeto de mensagem do LangChain e retorna uma string
    formatada e colorida/amigável para exibição no terminal.
    """
    if isinstance(message, HumanMessage):
        return f"👤 Você: {message.content}"
    
    elif isinstance(message, AIMessage):
        # Se a mensagem tiver chamadas de ferramentas associadas
        if message.tool_calls:
            tool_names = ", ".join([tool["name"] for tool in message.tool_calls])
            return f"🤖 Agente: [🔧 Acionando ferramenta(s): {tool_names}]"
        # Se for apenas texto
        return f"🤖 Agente: {message.content}"
    
    elif isinstance(message, ToolMessage):
        # Trunca o resultado da ferramenta para não poluir o terminal se for muito longo
        preview = message.content[:100].replace('\n', ' ')
        suffix = "..." if len(message.content) > 100 else ""
        return f"   [✅ Resultado da ferramenta '{message.name}': {preview}{suffix}]"
    
    elif isinstance(message, SystemMessage):
        return f"⚙️ Sistema (Prompt): {message.content}"
    
    else:
        return f"❓ Tipo Desconhecido: {message.content}"


def debug_state(state: dict):
    """
    Utilitário para imprimir todo o histórico atualizado do estado.
    Muito útil para colocar dentro dos nós (nodes) durante o desenvolvimento.
    """
    print("\n" + "="*40 + " DEBUG DO ESTADO " + "="*40)
    for msg in state.get("messages", []):
        print(format_message(msg))
    print("="*97 + "\n")