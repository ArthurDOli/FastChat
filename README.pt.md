# FastChat

O FastChat é um projeto full-stack de uma aplicação de chat em tempo real, desenvolvido em Python com o framework FastAPI. A aplicação demonstra um sistema de autenticação robusto e comunicação bidirecional utilizando WebSockets.

## Funcionalidades

- **Sistema de Autenticação Completo**:
  - **Registro e Login**
  - **Hashing de Senhas**
- **Chat em Tempo Real**:
  - **Comunicação via WebSockets**
  - **Notificações de Status**
  - **Broadcasta de Mensagens**

## Tecnologias Utilizadas

- **Backend:** Python, FastAPI
- **Frontend:** HTML, Wailwind CSS, JavaScript
- **Base de Dados:** SQLite com SQLAlchemy

## Instalação e Configuração

Siga os passos abaixo para configurar e executar o projeto localmente:

1.  **Clone o repositório:**

    ```bash
    git clone https://github.com/ArthurDOli/FastChat.git
    cd FastChat
    ```

2.  **Crie e ative um ambiente virtual:**

    ```bash
    python -m venv venv
    # No Windows
    venv\Scripts\activate
    # No macOS/Linux
    source venv/bin/activate
    ```

3.  **Instale as dependências:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure as variáveis de ambiente:**
    Crie um ficheiro `.env` na raiz do projeto e adicione as seguintes variáveis. Estas chaves são essenciais para a segurança dos tokens JWT. Utilize chaves diferentes para SECRET_KEY e REFRESH_SECRET_KEY.

    ```
    SECRET_KEY="sua_chave1"
    REFRESH_SECRET_KEY="sua_chave2"
    ALGORITHM="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    REFRESH_TOKEN_EXPIRE_MINUTES=10080
    ```

5.  **Crie o banco de dados:**
    Execute o script `database.py` uma vez para criar o arquivo `database.db` e as tabelas.

    ```bash
    python database.py
    ```

6.  **Execute a aplicação:**
    O projeto está configurado para usar o Uvicorn, um servidor ASGI de alta performance.
    ```bash
    uvicorn main:app --reload
    ```

## Estrutura do Projeto

```bash
/FastChat
|-- /static/
|   |-- logo.png
|-- /templates/
|   |-- chat.html
|   |-- register.html
|-- .env
|-- .gitignore
|-- auth.py
|-- chat.py
|-- database.py
|-- main.py
|-- models.py
|-- schemas.py
`-- ws_manager.py
```
