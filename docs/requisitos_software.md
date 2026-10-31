# Documento de Requisitos de Software (SRS)
## Gemini Notebook Simplificado (Docs Reviewer)

---

### 1. Visão Geral do Projeto

O objetivo deste projeto é desenvolver uma versão simplificada e de fácil uso do **Google NotebookLM** (denominado **Gemini Notebook Simplificado** ou **Docs Reviewer**), utilizando **Python** e **Streamlit**. 

A aplicação permitirá aos usuários organizar seus estudos, pesquisas ou trabalhos em pastas temáticas ("Notebooks"), fazer o upload de múltiplos documentos em cada pasta e interagir via chat inteligente com modelos generativos (família Gemini) com suporte a RAG (*Retrieval-Augmented Generation*), garantindo que as respostas sejam fundamentadas diretamente nos documentos fornecidos.

---

### 2. Stack Tecnológica e Justificativas

| Componente | Tecnologia Selecionada | Justificativa |
| :--- | :--- | :--- |
| **Linguagem** | Python 3.10+ | Linguagem padrão para ecossistemas de IA, dados e prototipagem ágil. |
| **Interface / Frontend** | **Streamlit** | Framework reativo rápido para construção de interfaces web completas em Python, com suporte nativo a chat (`st.chat_message`, `st.chat_input`), sidebars e galerias com colunas. |
| **Framework de IA & RAG** | **LangChain** (ou LlamaIndex) + `langchain-google-genai` | Padrão da indústria para pipelines de RAG: divisão em chunks (*text splitters*), orquestração de prompts, gerenciamento de contexto, embeddings e integração simplificada com a API do Google Gemini. |
| **Modelo de LLM & Embeddings** | **Google Gemini** (Gemini 1.5 Flash / Pro) & `text-embedding-004` | Alta janela de contexto, respostas precisas e integração rápida e econômica via Google AI Studio / Gemini API. |
| **Banco Vetorial (Vector Store)** | **ChromaDB** (Persistente local) | Leve, não requer servidor externo dedicado, suporta armazenamento em disco local e permite segmentação das coleções por Notebook (`notebook_{id}`) ou filtragem por metadados. |
| **Banco Relacional / Metadados** | **SQLite** (via SQLAlchemy) | Banco de dados relacional embarcado e sem servidor para controle de Notebooks, metadados dos arquivos carregados e persistência de sessões e mensagens do chat. |
| **Armazenamento de Arquivos** | Sistema de Arquivos Local (`./storage/notebooks/{id}/`) | Armazenamento seguro dos arquivos brutos (PDFs, TXTs, DOCXs, etc.) para referência e pré-visualização. |

---

### 3. Requisitos Funcionais (RF)

#### RF01 - Gerenciamento de Pastas / Notebooks
- **RF01.1 - Listagem de Notebooks:** A interface deve exibir uma listagem clara de todos os notebooks cadastrados, permitindo alternar facilmente entre eles.
- **RF01.2 - Criação de Notebook:** O usuário deve ser capaz de criar um novo notebook informando nome e descrição opcional.
- **RF01.3 - Exclusão de Notebook:** O usuário deve poder deletar um notebook existente. Ao deletar, o sistema deve remover os metadados do SQLite, os arquivos físicos associados e a coleção vetorial no ChromaDB.
- **RF01.4 - Notebook Ativo:** A aplicação deve manter um estado de sessão indicando qual notebook está selecionado no momento.

#### RF02 - Galeria de Documentos e Gestão de Fontes
- **RF02.1 - Galeria de Documentos:** Para o notebook selecionado, exibir uma galeria/painel com todos os documentos carregados (título, tipo do arquivo, data de upload, status de processamento e quantidade de fragmentos/chunks).
- **RF02.2 - Upload de Arquivos:** Suportar upload de múltiplos arquivos nos formatos:
  - PDF (`.pdf`)
  - Texto simples (`.txt`)
  - Markdown (`.md`)
  - Documentos Word (`.docx`)
- **RF02.3 - Pipeline de Processamento e Ingestão (RAG):**
  - Extrair o texto dos documentos enviados.
  - Dividir o texto em blocos semânticos (*chunking*, ex: `chunk_size=1000`, `chunk_overlap=200`).
  - Gerar embeddings via modelo Google Gemini e armazenar no ChromaDB associado ao ID do notebook e documento.
- **RF02.4 - Remoção de Documentos:** Permitir que o usuário remova um documento individualmente da galeria, limpando os vetores correspondentes no ChromaDB e os metadados no SQLite.
- **RF02.5 - Seleção Ativa de Fontes (Opcional/Fase 2):** Permitir marcar/desmarcar quais documentos do notebook farão parte da busca vetorial na conversa atual.

#### RF03 - Chat Interativo com RAG
- **RF03.1 - Interface Conversacional:** Campo de chat interativo (`st.chat_input`) com visualização de mensagens do usuário e do assistente (`st.chat_message`).
- **RF03.2 - Busca Semântica (Retrieval):** Ao enviar uma pergunta, o sistema recupera os fragmentos mais relevantes dos documentos do notebook ativo no ChromaDB.
- **RF03.3 - Geração com Citação de Fontes:** O Gemini gera a resposta baseada exclusivamente ou prioritariamente nos fragmentos resgatados, citando o nome do documento e a página/seção de onde a informação foi extraída.
- **RF03.4 - Streaming de Resposta:** As respostas devem ser transmitidas via *streaming* em tempo real para melhorar a experiência do usuário.
- **RF03.5 - Histórico de Mensagens Persistente:** O histórico de conversa deve ficar salvo no SQLite e recarregado sempre que o usuário selecionar o notebook correspondente.
- **RF03.6 - Limpeza do Chat:** Botão para resetar ou limpar o histórico de mensagens do notebook atual.

---

### 4. Requisitos Não Funcionais (RNF)

- **RNF01 - Usabilidade:** Interface intuitiva com layout inspirado no Google NotebookLM:
  - Barra lateral ou cabeçalho para navegação entre Notebooks.
  - Painel esquerdo/central dividido entre Galeria de Fontes e Área de Chat.
- **RNF02 - Desempenho e Latência:** A busca vetorial e a geração de respostas devem apresentar baixa latência com uso de modelos rápidos como `gemini-1.5-flash` ou `gemini-2.0-flash`.
- **RNF03 - Persistência Confiável:** Toda informação (pastas, arquivos e histórico) deve persistir entre reinicializações do app Streamlit.
- **RNF04 - Segurança e Configuração:** Chave da API do Google Gemini (`GEMINI_API_KEY`) isolada em arquivo `.env` ou `st.secrets`, sem exposição no código-fonte.
- **RNF05 - Extensibilidade:** Arquitetura desacoplada em módulos (Banco de Dados, RAG, Gerenciamento de Documentos, Interface Streamlit).

---

### 5. Modelo de Dados e Arquitetura de Armazenamento

#### 5.1. Banco de Dados Relacional (SQLite)

```sql
-- Tabela de Notebooks (Pastas)
CREATE TABLE notebooks (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Documentos / Fontes
CREATE TABLE documents (
    id TEXT PRIMARY KEY,
    notebook_id TEXT NOT NULL,
    name TEXT NOT NULL,
    file_type TEXT NOT NULL,
    file_path TEXT NOT NULL,
    chunk_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (notebook_id) REFERENCES notebooks(id) ON DELETE CASCADE
);

-- Tabela de Histórico do Chat
CREATE TABLE chat_messages (
    id TEXT PRIMARY KEY,
    notebook_id TEXT NOT NULL,
    role TEXT NOT NULL, -- 'user' ou 'assistant'
    content TEXT NOT NULL,
    sources TEXT, -- JSON com as citações / chunks utilizados
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (notebook_id) REFERENCES notebooks(id) ON DELETE CASCADE
);
```

#### 5.2. Banco Vetorial (ChromaDB)
- **Coleções:** Uma coleção por notebook (`notebook_{notebook_id}`) ou coleção única com metadado `notebook_id` para filtragem (`where={"notebook_id": notebook_id}`).
- **Metadados por Chunk:**
  - `document_id`: ID do documento original no SQLite.
  - `document_name`: Nome legível do arquivo.
  - `page`: Número da página (se aplicável, ex: PDFs).
  - `chunk_index`: Índice sequencial do fragmento.

---

### 6. Estrutura Proposta do Projeto

```plaintext
docs-reviewer/
├── docs/
│   └── requisitos_software.md     # Documento de requisitos (este documento)
├── storage/                       # Armazenamento local persistente
│   ├── app.db                     # Banco SQLite (pastas, metadados e chat)
│   ├── chromadb/                  # Dados vetoriais do ChromaDB
│   └── notebooks/                 # Arquivos originais organizados por ID de notebook
├── src/
│   ├── config.py                  # Configurações de ambiente, caminhos e constantes
│   ├── database/
│   │   ├── db.py                  # Conexão SQLite e inicialização
│   │   ├── models.py              # Modelos de dados (SQLAlchemy ou dataclasses)
│   │   └── repository.py          # Operações de CRUD para notebooks, docs e mensagens
│   ├── rag/
│   │   ├── ingestion.py           # Leitura de PDFs/textos, chunking e vetorização
│   │   ├── vector_store.py        # Gerenciamento de coleções ChromaDB
│   │   └── chain.py               # Prompt RAG, busca semântica e chamada ao Gemini
│   └── ui/
│       ├── components.py          # Componentes visuais (galeria, cards de documentos)
│       ├── sidebar.py             # Menu lateral de pastas e seleção de notebooks
│       └── chat_view.py           # Painel de conversação e streaming de respostas
├── .env.example                   # Exemplo de configuração de variáveis de ambiente
├── requirements.txt               # Dependências do projeto
└── app.py                         # Ponto de entrada da aplicação Streamlit
```

---

### 7. Plano de Implementação (Passo a Passo)

1. **Fase 1: Configuração do Ambiente e Estrutura Base**
   - Criação do ambiente virtual e `requirements.txt`.
   - Implementação da camada de banco de dados SQLite (`repository.py`).
2. **Fase 2: Gestão de Notebooks e Interface Básica**
   - Criação da sidebar no Streamlit para listar, criar e deletar notebooks.
3. **Fase 3: Galeria de Documentos e Ingestão de Dados**
   - Upload de PDFs/textos, extração de texto e indexação no ChromaDB.
   - Renderização visual da galeria de documentos com opção de exclusão.
4. **Fase 4: Motor de RAG e Chat Inteligente**
   - Conexão com Google Gemini API.
   - Pipeline de busca semântica com ChromaDB e geração com citações.
   - Integração com o chat do Streamlit com persistência e streaming.
5. **Fase 5: Refinamentos e Validação**
   - Testes com múltiplos documentos simultâneos.
   - Melhorias visuais no estilo do NotebookLM e tratamento de exceções.
