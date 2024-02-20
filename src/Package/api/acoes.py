import pandas as pd
import yfinance as yf
from datetime import datetime

def ajusta_ticker_yf(ativo_carteira):
     nomeAjustado = f"{ativo_carteira}.SA"
     return nomeAjustado

def obter_cotacao_acao(ativo_carteira):
    ativo_yf = ajusta_ticker_yf(ativo_carteira)
    try:
        ticker = yf.Ticker(ativo_yf)
        cotacao = round(ticker.get_fast_info().last_price, 2)

    except Exception as e:
            mensagem_erro = f'Erro Ticker YF: {str(e)}'
            print(mensagem_erro)
            return {'ativo': ativo_carteira, 'cotacao': None, 'data_atualizacao':datetime.now(),'erro': mensagem_erro}

    return {'ativo': ativo_carteira, 'cotacao': cotacao, 'data_atualizacao':datetime.now(), 'erro': None}


def att_acoes(acoes):
    resultados = []
    
    for a in acoes:
        registro = obter_cotacao_acao(a)
        resultados.append(registro)

    df_resultados = pd.DataFrame(resultados)
    return df_resultados
