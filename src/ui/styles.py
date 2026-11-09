CUSTOM_CSS = """
<style>
    /* Estilização Geral inspirada no Google NotebookLM */
    .stApp {
        background-color: #0e1117;
        color: #e0e0e0;
    }
    
    /* Otimização de espaçamento para manter a interface contida na tela */
    .block-container,
    [data-testid="stMainBlockContainer"] {
        padding-top: 2rem !important;
        padding-bottom: 5.5rem !important;
        padding-left: 2.5rem !important;
        padding-right: 2.5rem !important;
        max-width: 100% !important;
    }

    /* Reduz espaço do cabeçalho da página */
    header[data-testid="stHeader"] {
        height: 2.5rem !important;
        background: transparent !important;
    }

    /* Ajuste de espaçamento para divisores */
    hr {
        margin: 0.75rem 0 !important;
        border-color: #282f3f !important;
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

    /* ========================================================
       CONTAINER DO CHAT E BARRA DE ROLAGEM
       ======================================================== */

    .chat-scroll-container,
    div:has(> .chat-scroll-container) {
        display: none !important;
    }

    /* Container do chat com borda, cantos arredondados e altura ajustada à tela */
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.chat-scroll-container) {
        background-color: #121620 !important;
        border: 1px solid #282f3f !important;
        border-radius: 12px !important;
        height: clamp(380px, calc(100vh - 350px), 640px) !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25) !important;
        margin-bottom: 0.5rem !important;
    }

    /* Área interna rolável com barra de rolagem lateral */
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.chat-scroll-container) > div[data-testid="stVerticalBlock"] {
        overflow-y: auto !important;
        scroll-behavior: smooth !important;
        padding: 1rem !important;
        scrollbar-width: thin !important;
        scrollbar-color: #4b5563 #161b26 !important;
    }

    /* Estilização da barra de rolagem para WebKit (Chrome, Edge, Safari, Opera) */
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.chat-scroll-container) > div[data-testid="stVerticalBlock"]::-webkit-scrollbar,
    div[data-testid="stVerticalBlockBorderWrapper"] > div[data-testid="stVerticalBlock"]::-webkit-scrollbar {
        width: 8px !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:has(.chat-scroll-container) > div[data-testid="stVerticalBlock"]::-webkit-scrollbar-track,
    div[data-testid="stVerticalBlockBorderWrapper"] > div[data-testid="stVerticalBlock"]::-webkit-scrollbar-track {
        background: #161b26 !important;
        border-radius: 4px !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:has(.chat-scroll-container) > div[data-testid="stVerticalBlock"]::-webkit-scrollbar-thumb,
    div[data-testid="stVerticalBlockBorderWrapper"] > div[data-testid="stVerticalBlock"]::-webkit-scrollbar-thumb {
        background-color: #4b5563 !important;
        border-radius: 4px !important;
        border: 2px solid #161b26 !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:has(.chat-scroll-container) > div[data-testid="stVerticalBlock"]::-webkit-scrollbar-thumb:hover,
    div[data-testid="stVerticalBlockBorderWrapper"] > div[data-testid="stVerticalBlock"]::-webkit-scrollbar-thumb:hover {
        background-color: #6b7280 !important;
    }

    /* Mensagens do Chat */
    div[data-testid="stChatMessage"] {
        background-color: #181c26 !important;
        border: 1px solid #282f3f !important;
        border-radius: 10px !important;
        margin-bottom: 0.75rem !important;
        padding: 0.85rem !important;
    }

    /* Barra inferior de entrada do chat */
    div[data-testid="stBottom"] {
        background-color: #0e1117 !important;
    }
</style>
"""
