import sqlite3
from langchain_core.tools import tool

# ==========================================
# Setup do Banco de Dados Fake (Em memória)
# ==========================================
def init_fake_db():
    """Inicializa um banco SQLite em memória com alguns dados de exemplo."""
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE pedidos (
            id INTEGER PRIMARY KEY,
            cliente TEXT,
            status TEXT,
            valor REAL
        )
    """)
    # Inserindo dados falsos
    cursor.executemany(
        "INSERT INTO pedidos (cliente, status, valor) VALUES (?, ?, ?)",
        [
            ("João Silva", "Enviado", 150.50),
            ("Maria Souza", "Processando", 89.90),
            ("Empresa XYZ", "Entregue", 1200.00)
        ]
    )
    conn.commit()
    return conn

# Mantém a conexão aberta enquanto o agente roda
db_connection = init_fake_db()

# ==========================================
# Ferramenta para o Agente
# ==========================================
@tool
def consultar_status_pedido(nome_cliente: str) -> str:
    """
    Consulta o banco de dados da empresa para verificar o status e valor do pedido de um cliente.
    Use esta ferramenta quando o usuário perguntar sobre o seu pedido, envio ou compra.
    """
    cursor = db_connection.cursor()
    cursor.execute("SELECT status, valor FROM pedidos WHERE cliente LIKE ?", (f"%{nome_cliente}%",))
    resultado = cursor.fetchone()
    
    if resultado:
        status, valor = resultado
        return f"O pedido de '{nome_cliente}' encontra-se com status: '{status}'. Valor total: R$ {valor:.2f}."
    else:
        return f"Nenhum pedido encontrado para o cliente '{nome_cliente}'. Peça para ele verificar o nome digitado."