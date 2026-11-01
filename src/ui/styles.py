CUSTOM_CSS = """
<style>
    /* Estilização Geral inspirada no Google NotebookLM */
    .stApp {
        background-color: #0e1117;
        color: #e0e0e0;
    }
    
    /* Cabeçalhos e Títulos */
    .main-header {
        font-size: 1.8rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 0.95rem;
        color: #9aa0a6;
        margin-bottom: 1.5rem;
    }

    /* ========================================================
       ESTILIZAÇÃO DE BOTÕES (Tons Suaves e Alto Contraste)
       ======================================================== */

    /* Botões Padrão / Secundários (Branco Suavizado / Off-White) */
    div[data-testid="stButton"] > button:not([kind="primary"]),
    div[data-testid="stFormSubmitButton"] > button:not([kind="primary"]),
    div[data-testid="stPopover"] > button,
    button[kind="secondary"],
    [data-testid="baseButton-secondary"] {
        background-color: #e2e8f0 !important; /* Branco suavizado, sem brilho agressivo */
        border: 1px solid #cbd5e1 !important;
        border-radius: 8px !important;
        color: #0f172a !important; /* Texto escuro grafite para máxima legibilidade */
        font-weight: 600 !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.08) !important;
        transition: all 0.15s ease-in-out !important;
    }

    /* Garante que elementos de texto e parágrafos internos ao botão fiquem escuros */
    div[data-testid="stButton"] > button:not([kind="primary"]) p,
    div[data-testid="stFormSubmitButton"] > button:not([kind="primary"]) p,
    div[data-testid="stPopover"] > button p,
    button[kind="secondary"] p,
    [data-testid="baseButton-secondary"] p,
    div[data-testid="stButton"] > button:not([kind="primary"]) span,
    button[kind="secondary"] span {
        color: #0f172a !important;
        font-weight: 600 !important;
    }

    /* Estado Hover para botões claros */
    div[data-testid="stButton"] > button:not([kind="primary"]):hover,
    div[data-testid="stFormSubmitButton"] > button:not([kind="primary"]):hover,
    div[data-testid="stPopover"] > button:hover,
    button[kind="secondary"]:hover,
    [data-testid="baseButton-secondary"]:hover {
        background-color: #cbd5e1 !important; /* Levemente mais escuro ao passar o mouse */
        border-color: #94a3b8 !important;
        color: #020617 !important;
    }

    div[data-testid="stButton"] > button:not([kind="primary"]):hover p,
    div[data-testid="stFormSubmitButton"] > button:not([kind="primary"]):hover p,
    div[data-testid="stPopover"] > button:hover p,
    button[kind="secondary"]:hover p,
    [data-testid="baseButton-secondary"]:hover p {
        color: #020617 !important;
    }

    /* Estado Ativo / Foco */
    div[data-testid="stButton"] > button:not([kind="primary"]):active,
    button[kind="secondary"]:active {
        background-color: #94a3b8 !important;
        color: #000000 !important;
    }

    /* Botões Primários (Azul Google) */
    div[data-testid="stButton"] > button[kind="primary"],
    div[data-testid="stFormSubmitButton"] > button[kind="primary"],
    button[kind="primary"],
    [data-testid="baseButton-primary"] {
        background-color: #1a73e8 !important;
        color: #ffffff !important;
        border: 1px solid #1557b0 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.15) !important;
    }

    div[data-testid="stButton"] > button[kind="primary"] p,
    div[data-testid="stFormSubmitButton"] > button[kind="primary"] p,
    button[kind="primary"] p,
    [data-testid="baseButton-primary"] p {
        color: #ffffff !important;
        font-weight: 600 !important;
    }

    div[data-testid="stButton"] > button[kind="primary"]:hover,
    button[kind="primary"]:hover,
    [data-testid="baseButton-primary"]:hover {
        background-color: #1557b0 !important;
        border-color: #0d47a1 !important;
        color: #ffffff !important;
    }

    /* ========================================================
       CARDS E COMPONENTES VISUAIS
       ======================================================== */

    /* Cards da Galeria de Documentos */
    .doc-card {
        background: #1e222d;
        border: 1px solid #2d3342;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 14px;
        transition: transform 0.15s ease, border-color 0.15s ease;
    }
    .doc-card:hover {
        border-color: #4285f4;
        transform: translateY(-2px);
    }
    .doc-title {
        font-size: 1rem;
        font-weight: 600;
        color: #f1f3f4;
        word-break: break-all;
        margin-bottom: 6px;
    }
    .doc-meta {
        font-size: 0.8rem;
        color: #9aa0a6;
        display: flex;
        gap: 12px;
        margin-bottom: 10px;
    }
    
    /* Badges de Tipo de Arquivo */
    .badge-pdf {
        background-color: #ea433522;
        color: #ea4335;
        border: 1px solid #ea433566;
        padding: 2px 8px;
        border-radius: 6px;
        font-weight: bold;
        font-size: 0.75rem;
    }
    .badge-docx {
        background-color: #4285f422;
        color: #4285f4;
        border: 1px solid #4285f466;
        padding: 2px 8px;
        border-radius: 6px;
        font-weight: bold;
        font-size: 0.75rem;
    }
    .badge-md, .badge-txt {
        background-color: #34a85322;
        color: #34a853;
        border: 1px solid #34a85366;
        padding: 2px 8px;
        border-radius: 6px;
        font-weight: bold;
        font-size: 0.75rem;
    }

    /* Citações e Fontes no Chat */
    .citation-box {
        background: #1a1e29;
        border-left: 3px solid #4285f4;
        padding: 8px 12px;
        border-radius: 4px;
        margin: 6px 0;
        font-size: 0.85rem;
    }
    .citation-title {
        font-weight: 600;
        color: #8ab4f8;
    }
    .citation-snippet {
        color: #bdc1c6;
        font-style: italic;
    }
</style>
"""
