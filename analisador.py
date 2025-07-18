import re
from xml.dom.expatbuilder import TEXT_NODE

import pandas as pd
import re

def analisar(url):
    lista_failed = []
    dict_ips = {}
    with open(url, 'r') as arquivo:
        lista_erros = ['Did not receive identification string', 'Invalid user', 'Received disconnect']

        for linha in arquivo:
            erro_encontrado = None
            for erro in lista_erros:
                if erro in linha:
                    erro_encontrado = erro
                    break

            if erro_encontrado:
                match_ip = re.search(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', linha)
                match_hora = re.search(r'\d{2}:\d{2}:\d{2}', linha)

                if match_ip and match_hora:
                    ip = match_ip.group(0)
                    hora = match_hora.group(0)

                    if ip in dict_ips:
                        dict_ips[ip]['tentativas'] += 1
                        dict_ips[ip]['horario'].append(hora)
                        dict_ips[ip]['erro'].append(erro_encontrado)
                    else:
                        dict_ips[ip] = {
                            'tentativas': 1,
                            'horario': [hora],
                            'erro': [erro_encontrado]
                        }


        df = pd.DataFrame.from_dict(dict_ips, orient='index')
        df = df.reset_index().rename(columns={'index': 'ip'})
        df.to_csv("analisados.csv", index=False)

