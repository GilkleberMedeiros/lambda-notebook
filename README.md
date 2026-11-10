# Lambda Notebook — Revisor de Documentos com IA

Protótipo totalmente funcional de um revisor de documentos com assistente de IA, construído com Python e Streamlit. Permite que o usuário organize documentos em notebooks, envie arquivos de texto e converse com um assistente de IA que responde com base exclusivamente no conteúdo dos documentos indexados.

---

## ✨ Funcionalidades

### 📁 Gerenciamento de Notebooks
- Crie notebooks para organizar seus documentos por tema ou projeto.
- Visualize na barra lateral todos os seus notebooks com o contador de documentos de cada um.
- Exclua notebooks — incluindo seus documentos e histórico de chat — com um clique.

### 📚 Galeria de Documentos
- Upload de arquivos diretamente na interface.
- Suporte aos formatos **PDF**, **DOCX**, **TXT** e **MD**.
- Visualização dos documentos indexados com métricas de chunks e tipo de arquivo.
- Exclusão individual de documentos com limpeza automática do vector store.

### 💬 Chat com IA (Q&A)
- Interface de chat completa com histórico de mensagens por notebook.
- Respostas geradas pelo modelo Gemini fundamentadas nos documentos indexados.
- Citação das fontes consultadas em cada resposta (nome do arquivo e trecho relevante).
- Filtro de fontes ativas: escolha quais documentos devem compor o contexto da pergunta.
- Sugestões rápidas de perguntas para facilitar a exploração dos documentos.
- Limpeza do histórico de conversa por notebook.

### ⚙️ Configuração via Interface
- Informe sua **Gemini API Key** diretamente na barra lateral, sem necessidade de editar arquivos.
- Escolha o modelo LLM e o modelo de embeddings Gemini desejados (incluindo modelos recém-lançados, digitando o nome).
- **Modo Demonstrativo** ativo automaticamente quando nenhuma chave de API é configurada, com dados mockados para exploração da interface.

---

## 🧠 Arquitetura RAG

A aplicação utiliza a técnica **RAG (Retrieval-Augmented Generation)** para fundamentar as respostas da IA no conteúdo real dos documentos.

```
Documento → Chunking → Embedding → ChromaDB (Vector Store)
                                          ↓
Pergunta do Usuário → Recontextualização → Retrieval → Contexto → LLM → Resposta
```

### Recontextualização de Prompt
Antes de realizar a busca semântica, a pergunta do usuário passa por uma etapa de **recontextualização** com base no histórico da conversa. Isso resolve ambiguidades causadas por pronomes e referências implícitas (ex: *"e ele?"*, *"quanto custa isso?"*), gerando uma query de busca autocontida e mais precisa — resultando em um retrieval significativamente mais relevante.

---

## 🛠️ Tecnologias

| Camada | Tecnologia |
|---|---|
| Interface | [Streamlit](https://streamlit.io/) |
| Linguagem | Python 3.10+ |
| LLM & Embeddings | [Gemini](https://ai.google.dev/) via `langchain-google-genai` |
| Orquestração RAG | [LangChain](https://www.langchain.com/) |
| Vector Store | [ChromaDB](https://www.trychroma.com/) (persistente, local) |
| Banco de Dados | SQLite via [SQLAlchemy](https://www.sqlalchemy.org/) |
| Gerenciador de Pacotes | [uv](https://docs.astral.sh/uv/) |

---

## 🚀 Como Executar

### Pré-requisitos
- Python 3.10+
- [`uv`](https://docs.astral.sh/uv/getting-started/installation/) instalado
- Uma [Gemini API Key](https://aistudio.google.com/app/apikey) (opcional para modo demonstrativo)

### 1. Clone o repositório e instale as dependências

```bash
git clone <url-do-repositorio>
cd lambda-notebook

uv pip install -r requirements.txt
```

### 2. Configure as variáveis de ambiente (opcional)

Copie o arquivo de exemplo e preencha sua API Key:

```bash
cp .env.example .env
```

```env
LLM_API_KEY=sua_gemini_api_key_aqui
LLM_MODEL=gemini-3.5-flash-lite              # opcional, padrão: gemini-3.1-flash-lite
EMBEDDING_MODEL=models/gemini-embedding-2  # opcional
```

> Sem a variável `LLM_API_KEY`, a aplicação inicia em **Modo Demonstrativo** com dados fictícios pré-carregados. A chave também pode ser informada diretamente na barra lateral da interface.

### 3. Inicie a aplicação

```bash
uv run streamlit run app.py
```

Acesse em `http://localhost:8501`.

---

## 📂 Estrutura do Projeto

```plaintext
docs-reviewer/
├── app.py                          # Ponto de entrada da aplicação
├── src/
│   ├── config.py                   # Configurações globais e variáveis de ambiente
│   ├── services.py                 # Lógica de negócio (modo real)
│   ├── mock_services.py            # Serviços mockados (modo demonstrativo)
│   ├── utils.py                    # Utilitários gerais
│   ├── database/
│   │   ├── db.py                   # Configuração do SQLAlchemy e engine SQLite
│   │   ├── models.py               # Modelos ORM (Notebook, Document, ChatMessage)
│   │   └── repository.py          # Funções de acesso ao banco de dados
│   ├── rag/
│   │   ├── ingestion.py            # Carregamento, chunking e embedding de documentos
│   │   ├── vector_store.py         # Interface com o ChromaDB
│   │   └── chain.py                # Construção das chains LangChain e prompt templates
│   ├── storage/
│   │   ├── app.db                  # Banco de dados SQLite local
│   │   ├── chromadb/               # Dados persistidos do ChromaDB
│   │   └── notebook/               # Arquivos originais enviados pelos usuários
│   └── ui/
│       ├── sidebar.py              # Barra lateral (configuração, navegação de notebooks)
│       ├── gallery.py              # Galeria de documentos e upload
│       ├── chat.py                 # Interface de chat e Q&A
│       └── styles.py               # CSS customizado (tema escuro)
├── .streamlit/
│   └── config.toml                 # Configurações de tema do Streamlit
├── .env.example                    # Exemplo de variáveis de ambiente
├── pyproject.toml                  # Configuração do projeto uv
└── requirements.txt                # Dependências com hashes para reprodutibilidade
```

---

## ⚠️ Limitações

- **Apenas texto:** A aplicação processa exclusivamente documentos de texto. Não há suporte a conteúdo multimodal — imagens incorporadas em PDFs, áudios ou vídeos são ignorados tanto no momento da ingestão quanto na interface de chat.
- **Formatos suportados:** Apenas `.pdf`, `.docx`, `.txt` e `.md`. Outros formatos comuns como `.csv`, `.xlsx`, `.pptx` ou `.html` ainda não são suportados. 
