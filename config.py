"""Configurações do Sistema FuryCelula

Centro de configuração para constantes e parâmetros do aplicativo.
"""
import os

# Caminhos dos arquivos de dados
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
MISSOES_PATH = os.path.join(DATA_DIR, "missoes.json")
HISTORICO_PATH = os.path.join(DATA_DIR, "historico.json")
PERFIL_PATH = os.path.join(DATA_DIR, "perfil.json")

# Itens da Loja (Hardcoded por enquanto)
ITENS_LOJA = [
    {"id": "tema_default", "nome": "Tema Padrão", "tipo": "tema", "preco": 0, "descricao": "Volta ao visual original.", "css_class": ""},
    {"id": "tema_matrix", "nome": "Matrix Mode", "tipo": "tema", "preco": 50, "descricao": "Visual hacker verde e preto.", "css_class": "tema_matrix"},
    {"id": "tema_crimson", "nome": "Crimson Protocol", "tipo": "tema", "preco": 100, "descricao": "Visual agressivo vermelho e dourado.", "css_class": "tema_crimson"},
    {"id": "tema_ice", "nome": "Ice Glitch", "tipo": "tema", "preco": 150, "descricao": "Visual futurista azul e ciano.", "css_class": "tema_ice"},
    {"id": "tema_zen", "nome": "Zen Mode", "tipo": "tema", "preco": 75, "descricao": "Minimalista. Foco total.", "css_class": "tema_zen"},
    {"id": "mystery_box", "nome": "Caixa Misteriosa", "tipo": "consumivel", "preco": 50, "descricao": "Pode conter 0 ou 200 moedas!", "css_class": ""},
    {"id": "pocao_foco", "nome": "Poção de Foco", "tipo": "consumivel", "preco": 150, "descricao": "Ganha 100 XP instantaneamente!", "css_class": ""},
]

# Limites de validação
MAX_TITULO_LENGTH = 255
MIN_TITULO_LENGTH = 3
MAX_HISTORICO_ENTRIES = 1000  # Rotacionar após este número

# Status válidos para missões
STATUS_VALIDOS = ["aberta", "em_andamento", "concluída"]
STATUS_DEFAULT = "aberta"

# Configurações do Flask
FLASK_DEBUG = True
FLASK_SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-prod")
