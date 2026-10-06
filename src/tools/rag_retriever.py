import os
from langchain_core.tools import tool
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

# Inicializa a conexão com o banco vetorial local existente
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
db_dir = os.path.join(os.getcwd(), "chroma_db")

# Garante que não quebre se o banco ainda não foi criado
if os.path.exists(db_dir):
    vectorstore = Chroma(persist_directory=db_dir, embedding_function=embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
else:
    retriever = None

@tool
def buscar_documentos_internos(query: str) -> str:
    """
    Busca informações na base de conhecimento interna da empresa (Manuais, PDFs, Políticas).
    Use esta ferramenta SEMPRE que o usuário perguntar sobre regras internas, 
    manuais de produtos da empresa ou documentos corporativos.
    """
    if retriever is None:
        return "Erro: Banco de dados vetorial não encontrado. Execute o script de ingestão primeiro."
    
    # Realiza a busca vetorial (similaridade)
    docs = retriever.invoke(query)
    
    if not docs:
        return "Nenhuma informação relevante encontrada nos documentos internos."
    
    # Formata o contexto para o LLM ler
    contexto = "Contexto encontrado nos documentos internos:\n\n"
    for i, doc in enumerate(docs, 1):
        contexto += f"--- Trecho {i} ---\n{doc.page_content}\n\n"
        
    return contexto