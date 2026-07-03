# Automação de Extração de Dados (Kaggle e Airtable)

Este projeto é um script de automação em Python que realiza a extração de dados de múltiplas fontes: baixa um dataset do Kaggle utilizando Selenium e busca informações de duas APIs do Airtable. Posteriormente, processa e converte os arquivos para o formato CSV, executando todo o ciclo periodicamente.

## ✨ Funcionalidades

- **Login Automático**: Acessa o Kaggle com as credenciais fornecidas.
- **Download de Datasets**: Baixa arquivos `.zip` de uma página de dataset específica.
- **Extração de API**: Coleta dados de endpoints do Airtable.
- **Processamento de Arquivos**: Descompacta arquivos `.zip` e converte dados de JSON para XLSX e, finalmente, para CSV.
- **Limpeza Automática**: Remove arquivos temporários (`.zip`, `.xlsx`) após o uso.
- **Execução Periódica**: Roda a automação em um loop contínuo com intervalo de tempo configurável (padrão: 1 hora).

## 🛠️ Estrutura do Projeto

O código segue os princípios da Programação Orientada a Objetos (POO) para garantir organização, legibilidade e manutenibilidade. A lógica é dividida em classes com responsabilidades bem definidas:

- **`kaggleautomacao`**: Gerencia toda a interação com o site do Kaggle via Selenium, incluindo login, download e manipulação de arquivos.
- **`tabelaAPI`**: Responsável por fazer as requisições às APIs do Airtable e salvar os resultados.
- **`conversao`**: Cuida da conversão entre diferentes formatos de arquivo (JSON → XLSX → CSV).
- **`comecar`**: Orquestra a execução de todas as tarefas na sequência correta e gerencia o loop de execução periódica.

## 🚀 Começando

Siga as instruções abaixo para configurar e executar o projeto em seu ambiente local.

### Pré-requisitos

- Python 3.x
- Google Chrome instalado
- Git

### Instalação

1.  **Clone o repositório:**
    ```bash
    git clone <URL_DO_SEU_REPOSITORIO>
    cd <NOME_DO_REPOSITORIO>
    ```

2.  **Crie e ative um ambiente virtual (recomendado):**
    ```bash
    # Para Linux/macOS
    python3 -m venv venv
    source venv/bin/activate

    # Para Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Instale as dependências:**
    As dependências do projeto estão listadas no arquivo `requirements.txt`. Instale-as com o comando:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure as variáveis de ambiente:**
    Este projeto utiliza um arquivo `.env` para gerenciar configurações e credenciais.
    -   Renomeie o arquivo `.env.example` para `.env`.
    -   Abra o arquivo `.env` e preencha com suas informações:

    ```dotenv
    # Token da API do Airtable
    tokenAPI=SUA_CHAVE_API_AQUI

    # Credenciais do Kaggle
    KAGGLE_EMAIL=SEU_EMAIL_KAGGLE_AQUI
    KAGGLE_PASSWORD=SUA_SENHA_KAGGLE_AQUI

    # Caminho para a pasta onde os arquivos serão baixados e processados
    DOWNLOAD_PATH="C:/Caminho/Para/Sua/Pasta/Download"
    ```

    > ⚠️ **Importante:** O arquivo `.env` contém suas senhas e chaves de API. Ele já está incluído no `.gitignore` e **NUNCA** deve ser enviado para o GitHub.

### Uso

Após a configuração, execute o script principal a partir do seu terminal:

```bash
python main.py
```

O script iniciará o processo de automação e o repetirá a cada hora. Você pode alterar o intervalo no método `executar_periodo()` da classe `comecar`.

## 📖 Detalhamento das Funções

### Classe `kaggleautomacao`
- `__init__(...)`: Configura o Selenium WebDriver com opções para download automático na pasta definida no `.env`.
- `abrirKaggle()`: Navega para a URL do dataset no Kaggle.
- `login()`: Realiza o login no Kaggle usando as credenciais do arquivo `.env`.
- `download()`: Clica no botão para baixar o dataset como `.zip`.
- `esperarDownloadConcluir()`: Monitora a pasta de download para garantir que o arquivo foi baixado completamente.
- `extrairZip()`: Localiza e extrai o arquivo `.zip` baixado.
- `apagarZip()`: Remove o arquivo `.zip` após a extração.
- `fecharNavegador()`: Encerra a sessão do navegador para liberar recursos.

### Classe `tabelaAPI`
- `fazer_request()`: Conecta-se às APIs do Airtable e salva os dados retornados como arquivos `.json`.
- `erros()`: Encapsula a chamada de `fazer_request()` com tratamento de exceções.

### Classe `conversao`
- `converterJsonXlsx()`: Lê os arquivos `.json`, extrai os dados e os converte para o formato `.xlsx`.
- `converterXlsxCsv()`: Lê os arquivos `.xlsx` e os converte para o formato final `.csv`.
- `apagarXlsx()`: Remove os arquivos `.xlsx` intermediários.

### Classe `comecar`
- `iniciar()`: Executa o fluxo completo de automação, chamando os métodos das outras classes na ordem correta.
- `executar_periodo()`: Inicia um loop infinito que chama o método `iniciar()` em intervalos de tempo definidos.