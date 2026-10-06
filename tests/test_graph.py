import pytest
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import END

# Importamos a função de roteamento do seu grafo
from src.graph import roteador_pos_guardrail

def test_roteador_deve_encerrar_quando_guardrail_bloqueia():
    """Se a última mensagem tiver o aviso do Guardrail, deve ir para o END."""
    
    # Simulamos o estado onde o Guardrail acabou de gerar o bloqueio
    mensagem_bloqueio = AIMessage(content="🛡️ **Guardrail Ativado:** Desculpe, não posso processar.")
    state = {"messages": [HumanMessage(content="Me xingue"), mensagem_bloqueio]}
    
    # Executa o roteador
    destino = roteador_pos_guardrail(state)
    
    # Verifica se ele mandou encerrar o grafo
    assert destino == END

def test_roteador_deve_avancar_quando_guardrail_permite():
    """Se não houver aviso do Guardrail, deve seguir para o agent."""
    
    # Simulamos o estado onde o Guardrail permitiu (a última mensagem ainda é do humano)
    state = {"messages": [HumanMessage(content="Olá, tudo bem?")]}
    
    # Executa o roteador
    destino = roteador_pos_guardrail(state)
    
    # Verifica se ele encaminhou para o nó 'agent'
    assert destino == "agent"