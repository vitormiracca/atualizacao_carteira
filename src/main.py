### IMPORTS ###
from traceback import print_tb
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

from datetime import datetime
import pandas as pd
from Package.api import acoes, cryptos
from Package.utils import db_investimentos as db

print("""
#############################################################
      
            ATUALIZACAO PLANILHA DE COTAÇÕES ATUAIS

##############################################################   
      """)

######## SCRIPT - Atualizacao Cotacao Atual #########

caminho_csv = r'D:\Finanças Pessoais\Analytics\Cotacoes.csv'

ativos = db.tupla_ativos()
result_df = pd.DataFrame()

for categoria in ativos:
    if (categoria == 'bolsa'):
        df_acoes = acoes.att_acoes(ativos['bolsa'])
        result_df = pd.concat([result_df, df_acoes])
    elif (categoria == 'crypto'):
        df_crypto = cryptos.att_cryptos(ativos['crypto'])
        result_df = pd.concat([result_df, df_crypto])
    else:
        registros_ignorados = []
        for a in ativos['ignorados']:
            registro = {'ativo': a, 'cotacao': None, 'data_atualizacao':datetime.now(),'erro': 'Ativo Ignorado, sem automação'}
            registros_ignorados.append(registro)

        df_ignorados = pd.DataFrame(registros_ignorados)
        result_df = pd.concat([result_df, df_ignorados])

result_df.to_csv(caminho_csv, index=False)

print('''
######################
ATUALIZAÇÃO FINALIZADA
######################
''')



