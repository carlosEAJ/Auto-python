#imports das bibliotecas
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import json
from dotenv import load_dotenv
import os
import zipfile
import requests

class kaggleautomacao:
    def __init__(self):
        self.pasta_download = r"coloque o caminho da pasta de download aqui"
        opcoes = webdriver.ChromeOptions()
        opcoes.add_experimental_option("prefs", {
            "download.default_directory": self.pasta_download,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": False,          
            "safebrowsing.disable_download_protection": True,
        })
        
        #Faz o download do web driver compatível com o navegador
        opcoes.add_argument("--safebrowsing-disable-download-protection")
        opcoes.add_argument("--disable-features=DownloadBubble,DownloadBubbleV2")
        servico = Service(ChromeDriverManager().install())
        self.navegador = webdriver.Chrome(service=servico, options=opcoes)

        

    def abrirKaggle(self):
        
        self.navegador.get("https://www.kaggle.com/datasets/thomassimeo/volumetria-tempos-fictcios?select=HAGENT_2024-08-01.xlsx")
        

    def login(self):
        wait = WebDriverWait(self.navegador, 15)

        wait.until(EC.element_to_be_clickable((By.XPATH, '//a[contains(@href, "/account/login")]'))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Sign in with Email"]'))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@name="KAGGLE_EMAIL"]'))).send_keys('Email aqui')
        wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@name="KAGGLE_PASSWORD"]'))).send_keys('senha aqui')
        wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]'))).click()
        

    def download(self):
        wait = WebDriverWait(self.navegador, 15)
        
        
        wait.until(EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "Download")]/ancestor::button'))).click()
        wait.until(EC.presence_of_element_located((By.XPATH, '//li[@role="menuitem"]')))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//li[@role="menuitem" and .//p[contains(text(), "Download dataset as zip")]]'))).click()

    def esperarDownloadConcluir(self, timeout=60, estabilidade=2):
        tempo_inicial = time.time()
        tempo_sem_temp = None

        while True:
            arquivos = os.listdir(self.pasta_download)
            tem_temp = any(arquivo.endswith(".crdownload") for arquivo in arquivos)

            if tem_temp:
                tempo_sem_temp = None
            else:
                if tempo_sem_temp is None:
                    tempo_sem_temp = time.time()
                elif time.time() - tempo_sem_temp >= estabilidade:
                    break

            if time.time() - tempo_inicial > timeout:
                raise TimeoutError("Download não concluiu dentro do tempo esperado.")

            time.sleep(0.5)

    def extrairZip(self):
        
        arquivos_zip = [f for f in os.listdir(self.pasta_download) if f.endswith(".zip")]
        
        if not arquivos_zip:
            raise FileNotFoundError("Nenhum arquivo .zip encontrado")
        
        caminho_zip = os.path.join(self.pasta_download, arquivos_zip[0])
        
        with zipfile.ZipFile(caminho_zip, 'r') as zip_ref:
            zip_ref.extractall(self.pasta_download)
        
        print(f"Extraído: {caminho_zip}")

    def apagarZip(self):
        arquivos_zip = [f for f in os.listdir(self.pasta_download) if f.endswith(".zip")]
        
        if not arquivos_zip:
            print("Nenhum .zip encontrado para apagar.")
            return
        
        caminho_zip = os.path.join(self.pasta_download, arquivos_zip[0])
        os.remove(caminho_zip)
        print(f"Removido: {caminho_zip}")
    
    def fecharNavegador(self):
        self.navegador.quit()

class tabelaAPI:

    def __init__(self):
       load_dotenv()
       self.token = os.getenv("tokenAPI")
       self.pasta_download = r"coloque o caminho da pasta de download aqui"
        
    def fazer_request(self):
        urlFore = "https://api.airtable.com/v0/appMDw883DjY0pMej/Result%201"
        urlDepara = "https://api.airtable.com/v0/appnlzAmDtFtGBjyt/Result%201"

        headers = {
            "Authorization": f"Bearer {self.token}"
        }

        responseFore = requests.get(urlFore, headers=headers)
        responseDepara = requests.get(urlDepara, headers=headers)
        
        dados_fore = responseFore.json()
        dados_depara = responseDepara.json()

        if "records" in dados_fore:
            with open(os.path.join(self.pasta_download, "FORECAST.json"), "w", encoding="utf-8") as arquivo:
                json.dump(dados_fore, arquivo, ensure_ascii=False, indent=4)
        else:
            print("Erro ao fazer request: FORECAST")

        if "records" in dados_depara:
            with open(os.path.join(self.pasta_download, "DEPARA.json"), "w", encoding="utf-8") as arquivo:
                json.dump(dados_depara, arquivo, ensure_ascii=False, indent=4)
        else:
            print("Erro ao fazer request: DEPARA")
    
    def erros(self):
        try:
            self.fazer_request()
        except Exception as e:

            print(f"Erro ao fazer request: {e}")
            pass
    

class conversao:
    def __init__(self):
        self.pasta_download = r"coloque o caminho da pasta de download aqui"
    
    def converterJsonXlsx(self):
        arquivos = os.listdir(self.pasta_download)
            
        for arquivo in arquivos:
            if arquivo.endswith(".json"):
                caminho_completo = os.path.join(self.pasta_download, arquivo)
                with open(caminho_completo, "r", encoding="utf-8") as arquivo:
                    dados = json.load(arquivo)
                registros = dados["records"]
                linhas = [registro["fields"] for registro in registros]
                df = pd.DataFrame(linhas)
                caminho_novo = (os.path.splitext(caminho_completo)[0] + ".xlsx")
                df.to_excel(caminho_novo, index=False)
                print(f"Convertido: {caminho_completo} -> {caminho_novo}")

    def converterXlsxCsv(self):
        arquivos = os.listdir(self.pasta_download)
        
        for arquivo in arquivos:
            if arquivo.endswith(".xlsx"):
                caminho_completo = os.path.join(self.pasta_download, arquivo)
                df = pd.read_excel(caminho_completo)
                caminho_novo = (os.path.splitext(caminho_completo)[0] + ".csv")
                df.to_csv(caminho_novo, index=False)
                print(f"Convertido: {caminho_completo} -> {caminho_novo}")

    def apagarXlsx(self):
        arquivos_xlsx = [f for f in os.listdir(self.pasta_download) if f.endswith(".xlsx")]
        
        if not arquivos_xlsx:
            print("Nenhum .xlsx encontrado para apagar.")
            return
        for arquivo in arquivos_xlsx:
            caminho_xlsx = os.path.join(self.pasta_download, arquivo)
            os.remove(caminho_xlsx)
            print(f"Removido: {caminho_xlsx}")        
            
        
        
class comecar:
    def __init__(self):
        pass
    
    def iniciar(self):
       init = kaggleautomacao()
       init.abrirKaggle()
       init.login()
       init.download()
       init.esperarDownloadConcluir()
       init.extrairZip()
       init.apagarZip()
       init.fecharNavegador()
        
       table = tabelaAPI()
       table.erros()
        
       converte = conversao()
       converte.converterJsonXlsx()
       converte.converterXlsxCsv()
       converte.apagarXlsx()
       
    def executar_periodo(self, umaHora = 3600):
        while True:
            try:
                self.iniciar()
            except Exception as erro:
                print(f"Erro na execução: {erro}")
            time.sleep(umaHora)
            # também pode ser utilizado time.sleep(60 * 60)  
            
            



play = comecar()

play.executar_periodo()
