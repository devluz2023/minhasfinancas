import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

def ingest_documents():
    """Lê documentos da pasta data/, gera embeddings e salva no ChromaDB."""
    print("Iniciando ingestão de documentos...")
    
    # 1. Carrega o documento (ajuste o nome do arquivo)
    caminho_doc = "data/documento_interno.pdf"
    if not os.path.exists(caminho_doc):
        print(f"Erro: Crie a pasta data/ e adicione o arquivo '{caminho_doc}'")
        return

    loader = PyPDFLoader(caminho_doc)
    docs = loader.load()

    # 2. Divide em pedaços menores (Chunks)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    splits = text_splitter.split_documents(docs)

    # 3. Salva no banco vetorial local (pasta ./chroma_db)
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorstore = Chroma.from_documents(
        documents=splits, 
        embedding=embeddings, 
        persist_directory="./chroma_db"
    )
    
    print(f"✅ {len(splits)} chunks salvos com sucesso no ChromaDB!")

if __name__ == "__main__":
    ingest_documents()