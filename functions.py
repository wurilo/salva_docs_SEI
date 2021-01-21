from selenium import webdriver
from time import sleep
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re
import os
import sys
from tqdm import tqdm
from configparser import ConfigParser
from config import nova_configuracao, ler_configuracao

configfile_name = "config.ini"
config = ConfigParser()
config.read_file(open(configfile_name))

def salva_docs(unidade, p0, p1):
    URL_SEI = config.get("user", "url")
    usuario = config.get("user", "login")
    senha = config.get("user", "pwd")
    print('Iniciando pesquisa...\n')
    dir_driver = config.get("paths", "chromedriver_path")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(dir_driver, options=chrome_options)
    id_tabela_docs_gerados = "divInfraAreaTabela5"
    
    # Acesso do webdriver à URL
    driver.get(URL_SEI)

    # Preenchimento da tela de login
    driver.find_element_by_id("txtUsuario").send_keys(usuario)
    driver.find_element_by_id("pwdSenha").send_keys(senha)
    driver.find_element_by_xpath("//button[@type='submit']").click()
    sleep(0.8)

    # Seleciona a caixa da unidade no SEI
    caixas = Select(driver.find_element_by_xpath("//select[@name='selInfraUnidades']"))
    caixas.select_by_visible_text(unidade)

    sleep(0.8)

    # Seleciona o item "Estatísticas da unidade no menu"
    driver.find_element_by_xpath("//*[@id='main-menu']/li[16]/a/span").click()

    sleep(0.8)

    driver.find_element_by_xpath("//*[@id='main-menu']/li[16]/ul/li[1]/a").click()

    sleep(0.8)

    # Informa os parâmetros de pesquisa
    driver.find_element_by_id("txtPeriodoDe").send_keys(p0)
    driver.find_element_by_id("txtPeriodoA").send_keys(p1)
    driver.find_element_by_name("sbmPesquisar").click()

    sleep(0.8)

    # Retorna os resultados da pesquisa de documentos gerados
    tabela_docs_gerados = driver.find_element_by_id(id_tabela_docs_gerados)
    tabela_docs_gerados_html = tabela_docs_gerados.get_attribute('innerHTML')
    soup = BeautifulSoup(tabela_docs_gerados_html, 'html5lib')
    lista_nome_resultado = []
    for el in soup.find_all('td'):
        resultado1 = el.get_text()
        resultado2 = re.match('[A-Za-z!@#$&]', resultado1)
        if resultado2:
            lista_nome_resultado.append(resultado1)
    
    # Retorna o nome do documento
    n = 0
    lista_nome_resultado2 = []
    for nome in lista_nome_resultado:
        novo_nome = str(n) + ' - ' + nome
        lista_nome_resultado2.append(novo_nome)
        n += 1    
    n = 1

    # Retorna o quantitativo encontrado
    nome_links = []
    for el in soup.findAll('td', attrs={'class': re.compile("^totalEstatisticas")}):
        for link in el.findAll('a', attrs={'onclick': re.compile("^abrirDetalhe")}):
            nome_links.append(link.get_text())

    # Concatena o nome com o quantitativo de documentos gerados
    lista_nome_resultado3 = []
    x = 0
    y = 0
    for nome in range(len(lista_nome_resultado2)):
        novo_nome = str(lista_nome_resultado2[x]) + ' ::: ' + str(nome_links[y]) + ' documentos encontrados'
        lista_nome_resultado3.append(novo_nome)
        x += 1
        y += 1

    # Printa os nomes em menu
    print('Resultados encontrados: \n')
    for nome in lista_nome_resultado3:
        print(nome)
    
    # Lista os hiperlinks para cada tipo de documento encontrado
    links = []
    for el in soup.findAll('td', attrs={'class': re.compile("^totalEstatisticas")}):
        for link in el.findAll('a', attrs={'onclick': re.compile("^abrirDetalhe")}):
            link = str(link['onclick'])
            link = link[14:-3]
            links.append(link)
    
    # Solicita a inserção de escolha do usuário sobre o documento desejado
    print('\n')
    escolha = input('Insira o número do tipo de documento: \n')
    escolha = int(escolha)
    link_escolha = links[escolha]

    # Acessa a tabela de documentos gerados pelo driver e salva em uma variável objeto BS4
    URL_escolha = URL_SEI + link_escolha
    driver.get(URL_escolha)
    soup_tab_docs_gerados = BeautifulSoup(driver.page_source, 'lxml')
    quant_raps = int(nome_links[escolha])

    
    # Calcula a quantidade de telas e documentos gerados

    if quant_raps <= 50:
	    telas = 1
    else:
	    telas = math.ceil(quant_raps / 50)

    quant_telas = range(telas)
    lista_dados = []

    for tela in quant_telas:
        soup_tab_docs_gerados = BeautifulSoup(driver.page_source, 'lxml')
        prot_raps = soup_tab_docs_gerados.find_all('a', title=lista_nome_resultado[escolha])
        for rap in prot_raps:
            lista_dados.append(rap.get('href'))
        if tela < max(quant_telas): 
            driver.find_element_by_xpath("//*[@id='lnkInfraProximaPaginaSuperior']/img").click()
            time.sleep(0.8)
        tela =+ 1

    print('Número de links listados: ' + str(len(lista_dados)) + '\n')

    soup_documento = BeautifulSoup(driver.page_source, 'lxml')

    #Cria o diretório para armazenar os documentos em formato html
    diretorio_parente = '/home/mrl0/Documentos/SCRIPTS/'
    nome_periodo_0 = re.sub(r'[^\w]', '', p0)
    nome_periodo_1 = re.sub(r'[^\w]', '', p1)

    diretorio = unidade + '/' + lista_nome_resultado[escolha] + '/' + nome_periodo_0 + ' a ' + nome_periodo_1
    caminho = os.path.join(diretorio_parente, diretorio)

    if not os.path.exists(caminho):
        os.makedirs(caminho)
        print('Diretorio criado: ' + diretorio)

    # Loop de salvamento dos documentos

    with tqdm(total=len(lista_dados), file=sys.stdout) as pbar:
        for doc in lista_dados:
            driver.get('https://sei.antt.gov.br/sei/' + str(doc))
            soup_documento = BeautifulSoup(driver.page_source, 'lxml')
            titulo = driver.title
            titulo = re.sub('[^A-Za-z0-9]+', ' ', titulo)
            rap = open(os.path.join(caminho, titulo+".html"), "w")
            rap.write(str(soup_documento))
            rap.close
            pbar.set_description('Progresso:')
            pbar.update(1)
            sleep(1)

    driver.quit()

    return