from datetime import datetime
import ccxt
import pandas as pd

def obter_cotacao_crypto(symbol):
    exchange = ccxt.binance()

    try:
        ticker = exchange.fetch_ticker(symbol)
        cotacao = ticker['close']
        mensagem_erro = None
    
    except ccxt.NetworkError as e:
        cotacao = None
        mensagem_erro = f'NetworkError: {e}'
    except ccxt.ExchangeError as e:
        cotacao = None
        mensagem_erro = f'ExchangeError: {e}'
    except Exception as e:
        cotacao = None
        mensagem_erro = f'Exception: {e}'

    return {'ativo': symbol, 'cotacao': cotacao, 'data_atualizacao':datetime.now(), 'erro': mensagem_erro}

def att_cryptos(lista_crypto:list):
    registros = []
    for a in lista_crypto:
        att = obter_cotacao_crypto(a)
        registros.append(att)

    df_cryptos = pd.DataFrame(registros)
    return df_cryptos