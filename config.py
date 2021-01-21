import os
import configparser

#Cria o arquivo de configuração
def nova_configuracao():
    configfile_name = "config.ini"
    cfgfile = open(configfile_name, 'w')

    chromedriver = input('Insira o caminho do diretório do chromedriver:')
    dir_path = input('Insira o caminho do diretório raiz para salvar os arquivos:')
    login = input('Insira o seu login no SEI:')
    pwd = input('Insira a sua senha no SEI:')
    sei_URL = input("Insira a URL do SEI desejado: \n 'https://sei.antt.gov.br/'")

    #Adiciona o conteúdo ao arquivo de configuração
    Config = configparser.ConfigParser()
    Config.add_section("paths")
    Config.set("paths", "chromedriver_path", chromedriver)
    Config.set("paths", "save_files_path", dir_path)
    Config.add_section("user")
    Config.set("user", "login", login)
    Config.set("user", "pwd", pwd)
    Config.set("user", "url", sei_URL)
    Config.write(cfgfile)
    cfgfile.close()

    return

def ler_configuracao():
    #Carrega o arquivo de configuração
    Config = configparser.ConfigParser()
    Config.read_file(open("config.ini"))

    #Printa os dados
    print('Configurações:')
    print('----------------------------------------------')
    print('Diretório do chromedriver:')
    print(Config.get("paths", "chromedriver_path"))
    print('----------------------------------------------')
    print('Diretório raiz para salvar arquivos:')
    print(Config.get("paths", "save_files_path"))
    print('----------------------------------------------')
    print('Login cadastrado:')
    print(Config.get("user", "login"))
    print('----------------------------------------------')
    print('URL do SEI:')
    print(Config.get("user", "url"))
    print('----------------------------------------------')

    return