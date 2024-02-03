import requests
import pandas as pd
import datetime
import time
import re


API_key = "JCWFS7OOOD2KUK2M"


#Functions

def latest_price_stocks_df(symbols: list) -> pd.DataFrame:

    print("##### INICIANDO LEITURA DE DADOS DOS ULTIMOS PRECOS DE ACOES BR (API) #####\n")
    df_cotacoes = pd.DataFrame()
    ### Bloco validacao do simbolo (melhorar)
    ###
    for symbol in symbols:
        df = latest_price_stock_request(symbol)
        df_cotacoes = pd.concat([df_cotacoes, df])

        print(f"- {symbol} -> Cotação Atualizada\n")

        time.sleep(25)
        
        #Incluir abend de df com symbolo e sem cotacaos
        # tratativa de erro -> print(f"### {symbol} !ERROR!-> Falaha na execucao: latest_price_stock_request(symbol)\n\n")
    print("\n##### DF COTACOES (ACOES) GERADO COM SUCESSO #####\n")
    return df_cotacoes

def latest_cryptos_df(symbols: list) -> pd.DataFrame:

    print("##### INICIANDO LEITURA DE DADOS DOS ULTIMOS PRECOS DE CRYPTOS (API) #####\n")
    df_cotacoes = pd.DataFrame()
    ### Bloco validacao do simbolo (melhorar)
    ###
    for symbol in symbols:
        listSimbol = re.split('/', symbol)


        df = latest_crypto_request(listSimbol[0], listSimbol[1])
        df_cotacoes = pd.concat([df_cotacoes, df])

        print(f"- {symbol} -> Cotação Atualizada\n")

        time.sleep(25)
        
        #Incluir abend de df com symbolo e sem cotacaos
        # tratativa de erro -> print(f"### {symbol} !ERROR!-> Falaha na execucao: latest_price_stock_request(symbol)\n\n")
    print("\n##### DF COTACOES (CRYPTO) GERADO COM SUCESSO #####")
    return df_cotacoes
    

## Unique Url Requests

def latest_price_stock_request(symbol: str) -> pd.DataFrame:
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_key}'
    r = requests.get(url)
    data = r.json()

    df = pd.DataFrame.from_dict(data, orient='index')
    df = df.astype(
        {
            '01. symbol':'string', 
            '05. price':'float64', '08. previous close': 
            'float64'
            }).rename(
        {'01. symbol':'cdAtivo', 
         '05. price':'cotacao', 
         '08. previous close': 'cotacao_Anterior'
         }, axis = 1)
    df = df[['cdAtivo', 'cotacao']]
    df['dataAtualizacao'] = datetime.date.today()

    return df

def weekly_stock_request(symbol: str) -> pd.DataFrame:
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol={symbol}&apikey={API_key}'
    r = requests.get(url)
    data = r.json()['Weekly Time Series']
    df_api = pd.DataFrame.from_dict(data, orient='index')

    df_api = (df_api.rename({
        '1. open':'Abertura', 
        '2. high':'Maxima', 
        '3. low': 'Minima',
        '4. close': 'cotacao'
        }, axis = 1)).astype(
            {
                'Abertura':'float64', 
                'Maxima':'float64', 
                'Minima': 'float64',
                'cotacao': 'float64'
                })
    df_api = (df_api[['Abertura','Maxima', 'Minima', 'cotacao']])
    df_api = df_api.rename_axis('Data')
    df_api['Ativo'] = f"{symbol}"

    return df_api

def monthly_stocks_request(symbol: str):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol={symbol}&apikey={API_key}'

def latest_crypto_request(symbol: str, market: str):
    url = f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={symbol}&to_currency={market}&apikey={API_key}'
    r = requests.get(url)
    data = r.json()

    df = pd.DataFrame.from_dict(data, orient='index')
    df = df.astype(
                {
                    '1. From_Currency Code':'string', 
                    '3. To_Currency Code':'string', 
                    '5. Exchange Rate':'float64',
                    '6. Last Refreshed':'datetime64[D]',
                }
                ).rename(
                {
                    '1. From_Currency Code':'cdMoeda', 
                    '3. To_Currency Code':'cdMercado', 
                    '5. Exchange Rate': 'cotacao',
                    '6. Last Refreshed': 'dataAtualizacao'
                }, axis = 1
                )
    df['cdAtivo'] = df['cdMoeda'].map(str) + '/' + df['cdMercado'].map(str)
    df = df[['cdAtivo', 'cotacao', 'dataAtualizacao']]
    return df

def monthly_crypto_request(symbol: str, market: str): 
    url = f'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_MONTHLY&symbol={symbol}&market={market}&apikey={API_key}'
    r = requests.get(url)
    data = r.json()
    return data

def symbol_search_request(keyword: str): 
    url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={keyword}&apikey={API_key}'
    r = requests.get(url)
    data = r.json()
    return data

