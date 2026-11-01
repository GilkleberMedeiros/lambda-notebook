# 📓 Gemini Notebook (Docs Reviewer) - Protótipo de Interface

Protótipo interativo do **Google NotebookLM** desenvolvido com **Python** e **Streamlit**, com interface completa e dados mockados para navegação, criação/exclusão de pastas (notebooks), galeria de documentos e chat com fontes citadas.

---

## 🎨 Componentes da Interface

- **📁 Pastas (Notebooks):**
  - Barra lateral com listagem dos notebooks cadastrados e contador de documentos.
  - Seleção do notebook ativo em destaque.
  - Formulário para criação de novos notebooks.
  - Botão de exclusão (lixeira) para remoção de pastas.

- **📚 Galeria de Fontes:**
  - Exibição em cards com tipo do arquivo (`PDF`, `DOCX`, `TXT`, `MD`), data, tamanho em KB e chunks indexados.
  - Caixa de upload para adicionar novos documentos simulados à galeria.
  - Visualização de detalhes e exclusão individual de arquivos.

- **💬 Chat & Q&A:**
  - Histórico de mensagens entre usuário e assistente.
  - Citações de fontes em cartões expansíveis (`🔍 Fontes consultadas`).
  - Streaming simulado de respostas em tempo real.
  - Filtro opcional de fontes ativas por consulta.
  - Botões com sugestões rápidas de perguntas.
  - Ação para limpar o histórico do notebook ativo.

---

## 📦 Como Executar com `uv`

```bash
# 1. Instalar as dependências via uv
uv pip install -r requirements.txt

# 2. Iniciar a aplicação Streamlit
uv run streamlit run app.py
```

O aplicativo será aberto no navegador em `http://localhost:8501`.

---

## 📂 Estrutura do Projeto

```plaintext
docs-reviewer/
├── docs/
│   └── requisitos_software.md     # Documento de requisitos de software (SRS)
├── src/
│   ├── mock_data.py               # Estrutura e controle de estado dos dados mockados
│   └── ui/
│       ├── styles.py              # CSS com paleta escura e botões suaves de alto contraste
│       ├── sidebar.py             # Barra lateral com gestão de notebooks
│       ├── gallery.py             # Galeria de documentos e upload
│       └── chat.py                # Painel de conversação e fontes citadas
├── .streamlit/
│   └── config.toml                # Configurações de tema Streamlit
├── pyproject.toml                 # Configuração do projeto uv
├── requirements.txt               # Dependências enxutas (Streamlit)
└── app.py                         # Ponto de entrada da aplicação
```
