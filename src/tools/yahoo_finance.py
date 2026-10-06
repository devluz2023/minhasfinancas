import os
import json
import yfinance as yf
import matplotlib.pyplot as plt
from langchain_core.tools import tool

@tool
def buscar_dados_yahoo_finance(ticker: str, periodo: str = "1mo") -> str:
    """
    Busca dados financeiros de uma empresa e gera um gráfico de ações usando o Yahoo Finance.
    Use esta ferramenta quando o usuário pedir dados de ações, cotações, indicadores financeiros ou gráficos.
    O ticker deve ser o símbolo oficial (ex: AAPL, MSFT). Para ações brasileiras na B3, adicione '.SA' (ex: PETR4.SA, VALE3.SA).
    O período padrão é '1mo' (1 mês), mas pode ser '1y' (1 ano), '5d' (5 dias), etc.
    """
    try:
        acao = yf.Ticker(ticker)
        
        # 1. Busca as informações básicas e filtra os dados mais importantes para o JSON
        info = acao.info
        dados_resumidos = {
            "nome": info.get("shortName", ticker),
            "setor": info.get("sector", "N/A"),
            "preco_atual": info.get("currentPrice", "N/A"),
            "moeda": info.get("financialCurrency", "N/A"),
            "market_cap": info.get("marketCap", "N/A"),
            "dividend_yield": info.get("dividendYield", "N/A")
        }
        json_dados = json.dumps(dados_resumidos, indent=2, ensure_ascii=False)
        
        # 2. Busca o histórico e gera o gráfico
        hist = acao.history(period=periodo)
        
        if hist.empty:
            return f"Dados encontrados:\n{json_dados}\n\n(Aviso: Não foi possível gerar o gráfico pois não há dados históricos para o período '{periodo}')"
        
        # Garante que a pasta 'data/' exista na raiz do projeto
        os.makedirs("data", exist_ok=True)
        
        # Limpa o nome do arquivo (remove o .SA para não dar erro no Windows/Linux)
        nome_arquivo = ticker.replace(".", "_")
        caminho_grafico = f"data/{nome_arquivo}_grafico.png"
        
        # Plota o gráfico usando Matplotlib
        plt.figure(figsize=(10, 5))
        plt.plot(hist.index, hist['Close'], label='Preço de Fechamento', color='green')
        plt.title(f"Histórico de Preços - {ticker} ({periodo})")
        plt.xlabel("Data")
        plt.ylabel("Preço")
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.7)
        
        # Salva a imagem e fecha a figura para liberar memória
        plt.savefig(caminho_grafico)
        plt.close()
        
        # 3. Retorna o texto formatado para o LLM ler e repassar ao usuário
        return (
            f"Dados Financeiros (em JSON):\n{json_dados}\n\n"
            f"✅ O gráfico de evolução de preços foi gerado com sucesso e salvo no arquivo: '{caminho_grafico}'"
        )
        
    except Exception as e:
        return f"Erro ao buscar dados da ação '{ticker}' no Yahoo Finance: {str(e)}"