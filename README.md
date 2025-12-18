# 🧠 Projeto MONAN
**Sistema Inteligente de Apoio ao Diagnóstico do TEA**

Este repositório contém a estrutura base ("esqueleto") para o desenvolvimento do Projeto Integrador. O sistema já possui autenticação, interface visual (Dashboard) e gestão de base de dados configurada, permitindo que a equipa foque na implementação da lógica de negócio e integração com IA.

---

##  1. Configuração do Ambiente

Siga estes passos para colocar o projeto a funcionar na sua máquina local.

### Pré-requisitos
* Python 3.10 ou superior.

### Passo a Passo

1.  **Criar o Ambiente Virtual** (Isolamento das dependências)
    * **Windows:**
        ```bash
        python -m venv venv
        venv\Scripts\activate
        ```
    * **Linux/Mac:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

2.  **Instalar Dependências**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configurar a Base de Dados**
    Cria as tabelas iniciais definidas nos Modelos:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

4.  **Criar Utilizador Administrador**
    Para aceder ao sistema e ao painel administrativo:
    ```bash
    python manage.py createsuperuser
    ```
    *(Siga as instruções para definir email e senha)*.

5.  **Rodar o Servidor**
    ```bash
    python manage.py runserver
    ```
    Acesse no navegador: `http://127.0.0.1:8000/`

---

##  2. Estrutura do Projeto

Entenda onde trabalhar:

* **`monan/`**: Pasta de configurações globais (`settings.py`, `urls.py`).
* **`core/`**: A aplicação principal.
    * `models.py`: Definição das tabelas (Usuários, Arquivos EEG, Análises).
    * `views.py`: A lógica das páginas (Dashboard, Upload, Perfil).
    * `forms.py`: Validação de formulários.
* **`templates/`**: Arquivos HTML (Frontend).
* **`static/`**: Arquivos CSS, Imagens e JavaScript.
* **`uploads/`**: Pasta onde os arquivos EEG enviados serão salvos.

---

##  3. Guia de Desenvolvimento (Suas Missões)

O código atual está funcional, mas incompleto propositalmente. Abaixo estão as tarefas técnicas mapeadas com o documento do Projeto Integrador:

###  Missão 1: Validação de Segurança (Etapa 3)
* **Arquivo alvo:** `core/views.py` (função `upload_file`).
* **Objetivo:** O sistema atual aceita qualquer arquivo. Você deve implementar:
    1.  Verificação rigorosa da extensão (`.gdf` ou `.dta`).
    2.  Renomeação automática do arquivo usando UUID para evitar sobrescrita.

###  Missão 2: Integração com IA (Etapa 4)
* **Arquivo alvo:** Criar `services/ml_api.py`.
* **Objetivo:** O botão "Analisar" no histórico apenas muda o status visual. Você deve:
    1.  Criar a lógica que lê o arquivo físico.
    2.  Integrar com o script do WEKA (ou criar um simulador de IA conforme o PDF).
    3.  Atualizar o resultado (`classification` e `confidence`) na base de dados.

###  Missão 3: Gerador de Laudos (Etapa 5)
* **Arquivo alvo:** Criar `services/report_generator.py`.
* **Objetivo:**
    1.  Usar a biblioteca `reportlab`.
    2.  Desenhar um PDF que contenha os dados do utilizador e o resultado da análise.
    3.  Implementar a marca d'água de segurança e o aviso ético.

###  Missão 4: Logging (Etapa 1 e 2)
* **Arquivo alvo:** `monan/settings.py` e criar `utils/logger.py`.
* **Objetivo:** Configurar o sistema para gravar erros e ações importantes num arquivo de texto (ex: `system.log`).



---
**Bom trabalho e boa codificação!** 🚀
