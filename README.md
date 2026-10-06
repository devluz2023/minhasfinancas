minhasfinancas/
├── .env                        # Chaves de API (OPENAI_API_KEY, TAVILY_API_KEY, etc.)
├── .gitignore
├── requirements.txt            # ou pyproject.toml (Poetry/UV)
├── README.md
├── src/
│   ├── __init__.py
│   ├── main.py                 # Ponto de entrada (CLI, FastAPI ou LangServe)
│   ├── config.py               # Carregamento de variáveis de ambiente e configurações globais
│   ├── state.py                # Definição do Estado do grafo (TypedDict ou Pydantic)
│   ├── graph.py                # Montagem, roteamento (edges) e compilação do StateGraph
│   ├── llm.py                  # Inicialização dos modelos fundacionais (ChatOpenAI, ChatAnthropic)
│   ├── prompts/                
│   │   ├── __init__.py
│   │   └── system_prompts.py   # Templates de prompts usando LangChain (PromptTemplate)
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── web_search.py       # Ferramentas customizadas decoradas com @tool
│   │   └── database.py         # Conexões com bancos de dados ou APIs externas
│   ├── nodes/
│   │   ├── __init__.py
│   │   ├── agent_node.py       # Nó principal que invoca o LLM
│   │   ├── tool_node.py        # Nó responsável por executar as ferramentas
│   │   └── human_node.py       # Nó para human-in-the-loop (aprovação)
│   └── utils/
│       └── helpers.py          # Funções auxiliares (formatação, parsing de logs, etc.)
└── tests/
    ├── __init__.py
    ├── test_nodes.py           # Testes unitários para funções isoladas dos nós
    └── test_graph.py           # Testes de integração do fluxo completo do LangGraph