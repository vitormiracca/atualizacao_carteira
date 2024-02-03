import pandas as pd
import os

def valida_acao(ativo):
    return (len(ativo) < 11) and ('3' in ativo or '4' in ativo or '11' in ativo or '5' in ativo)

def valida_crypto(ativo):
    return (ativo.find('/') >= 0) & (len(ativo) <=11)

def tupla_ativos() -> tuple:

    ativos_crypto = []
    ativos_bolsa = []
    ativos_ignorados = []

    tupla_ativos = {
        'bolsa' : ativos_bolsa, 
        'crypto' : ativos_crypto,
        'ignorados' : ativos_ignorados
        }

    mov = pd.read_excel('D:\Finanças Pessoais\Analytics\db_investimentos.xlsx', sheet_name='Movimentacoes', usecols=[2])
    ativos = mov.Ativo.unique()

    for ativo in ativos:
        ativo = str(ativo)
        if valida_acao(ativo):
            ativos_bolsa.append(ativo)

        elif valida_crypto(ativo):
            # nomeAjustado = ativo.replace('/', '-')
            ativos_crypto.append(ativo)

        else:
            ativos_ignorados.append(ativo)

    return tupla_ativos