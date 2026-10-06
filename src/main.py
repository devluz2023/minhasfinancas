import os
from dotenv import load_dotenv
from typing import Dict, Any

# Carrega as chaves de API do arquivo .env (ex: OPENAI_API_KEY, TAVILY_API_KEY)
load_dotenv()

# Importa o grafo compilado da nossa aplicação
# (Isso vai funcionar assim que criarmos o arquivo graph.py)
try:
    from src.graph import app
except ImportError:
    print("Aviso: O arquivo src/graph.py ou o objeto 'app' ainda não foi criado.")
    app = None

def main():
    print("🤖 Agente LangGraph Iniciado!")
    print("Digite 'sair' ou 'exit' para encerrar a conversa.")
    print("-" * 50)

    # Configuração de thread para manter a memória da conversa (caso adicione Checkpointers depois)
    config = {"configurable": {"thread_id": "sessao_terminal_1"}}

    while True:
        try:
            user_input = input("\nVocê: ")
            
            if user_input.lower() in ['sair', 'exit', 'quit']:
                print("Encerrando o agente. Até logo!")
                break
            
            if not user_input.strip():
                continue

            if app is None:
                print("Erro: O Grafo (app) não está disponível. Conclua a criação do graph.py primeiro.")
                continue

            # O estado inicial injeta a mensagem do usuário na lista de mensagens
            initial_state = {"messages": [("user", user_input)]}

            print("\nAgente: ", end="")
            
            # Executa o grafo utilizando stream para podermos ver os passos acontecendo
            for event in app.stream(initial_state, config=config):
                # 'event' é um dicionário com o nome do nó e a atualização do estado
                for node_name, state_update in event.items():
                    # Para debug, podemos imprimir qual nó está executando (opcional)
                    # print(f"[{node_name}]...") 
                    
                    if "messages" in state_update:
                        # Pega a última mensagem adicionada ao estado
                        last_message = state_update["messages"][-1]
                        
                        # Se for uma mensagem do assistente, imprimimos na tela
                        if last_message.type == "ai" and last_message.content:
                            print(last_message.content)
                        # Se for uma chamada de ferramenta (tool call)
                        elif last_message.type == "ai" and last_message.tool_calls:
                            print(f"\n[🔧 Usando ferramenta: {last_message.tool_calls[0]['name']}]")
                        # Se for o resultado de uma ferramenta
                        elif last_message.type == "tool":
                            print(f"[✅ Ferramenta concluída]")

        except KeyboardInterrupt:
            print("\nEncerrando o agente (Ctrl+C). Até logo!")
            break
        except Exception as e:
            print(f"\nOcorreu um erro: {e}")

if __name__ == "__main__":
    main()