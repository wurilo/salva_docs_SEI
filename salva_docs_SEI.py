from configparser import ConfigParser
from config import nova_configuracao, ler_configuracao
from functions import salva_docs
import os


#Teste e ajuste de configurações
configfile_name = "config.ini"
config = ConfigParser()

#Checa se há um arquivo de configuração
if not os.path.isfile(configfile_name):
    #Cria arquivo de configuração se não houver um
    nova_configuracao()
else:
    #Printa os dados de configuração atual e confirma
    ler_configuracao()
    manter_conf = input('Deseja manter a configuração atual? (s/n) \n')
    if manter_conf == 'n':
        nova_configuracao()

config.read_file(open(configfile_name))
print('\n')


unidade = input('Insira a sigla da unidade pesquisada (ex.: GEENG): \n')
print('\n')
p0 = input('Qual é a data inicial da pesquisa? (dd/mm/aaaa): \n')
print('\n')
p1 = input('Qual é a data final da pesquisa? (dd/mm/aaaa): \n')
print('\n')

salva_docs(unidade, p0, p1)




