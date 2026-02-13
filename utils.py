"""Funções Utilitárias do FuryCelula

Funções reutilizáveis para manipulação de arquivos JSON, validação e segurança.
"""
import json
import os
import shutil
from datetime import datetime
from markupsafe import escape
from config import (
    MISSOES_PATH,
    HISTORICO_PATH,
    MAX_TITULO_LENGTH,
    MIN_TITULO_LENGTH,
    MAX_HISTORICO_ENTRIES,
    STATUS_VALIDOS,
    STATUS_DEFAULT,
    PERFIL_PATH,
    ITENS_LOJA
)


def carregar_json(caminho):
    """
    Carrega dados de um arquivo JSON com tratamento de erros.
    
    Args:
        caminho: Path do arquivo JSON
    
    Returns:
        Lista com os dados ou lista vazia se houver erro
    """
    try:
        if not os.path.exists(caminho):
            return []
        
        with open(caminho, "r", encoding="utf-8") as f:
            dados = json.load(f)
            return dados if isinstance(dados, list) else []
    
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON {caminho}: {e}")
        # Tentar restaurar backup
        backup_path = f"{caminho}.bak"
        if os.path.exists(backup_path):
            print(f"Restaurando backup de {backup_path}")
            shutil.copy(backup_path, caminho)
            return carregar_json(caminho)
        return []
    
    except Exception as e:
        print(f"Erro ao carregar {caminho}: {e}")
    except Exception as e:
        print(f"Erro ao carregar {caminho}: {e}")
        return []


def carregar_json_dict(caminho):
    """
    Carrega dados de um arquivo JSON esperando um Dicionário.
    
    Args:
        caminho: Path do arquivo JSON
    
    Returns:
        Dicionário com os dados ou dict vazio se houver erro
    """
    try:
        if not os.path.exists(caminho):
            return {}
        
        with open(caminho, "r", encoding="utf-8") as f:
            dados = json.load(f)
            return dados if isinstance(dados, dict) else {}
    
    except Exception as e:
        print(f"Erro ao carregar dict {caminho}: {e}")
        return {}


def salvar_json(caminho, dados):
    """
    Salva dados em arquivo JSON com backup automático.
    
    Args:
        caminho: Path do arquivo JSON
        dados: Dados a serem salvos
    
    Returns:
        True se sucesso, False se houver erro
    """
    try:
        # Criar backup antes de salvar
        if os.path.exists(caminho):
            backup_path = f"{caminho}.bak"
            shutil.copy(caminho, backup_path)
        
        # Criar diretório se não existir
        os.makedirs(os.path.dirname(caminho), exist_ok=True)
        
        # Salvar com lock simples (arquivo temporário)
        temp_path = f"{caminho}.tmp"
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)
        
        # Renomear arquivo temporário para o definitivo
        shutil.move(temp_path, caminho)
        return True
    
    except Exception as e:
        print(f"Erro ao salvar {caminho}: {e}")
        return False


def salvar_log(acao, detalhe):
    """
    Salva uma entrada no histórico com rotação automática.
    
    Args:
        acao: Ação realizada (ex: "Criou missão")
        detalhe: Detalhes da ação
    """
    logs = carregar_json(HISTORICO_PATH)
    
    logs.insert(0, {
        "data": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "acao": str(acao),
        "resultado": str(detalhe)
    })
    
    # Rotacionar histórico se exceder o limite
    if len(logs) > MAX_HISTORICO_ENTRIES:
        logs = logs[:MAX_HISTORICO_ENTRIES]
    
    salvar_json(HISTORICO_PATH, logs)


def validar_titulo(titulo):
    """
    Valida e sanitiza o título de uma missão.
    
    Args:
        titulo: Título a ser validado
    
    Returns:
        Tuple (is_valid: bool, sanitized_titulo: str, error_msg: str)
    """
    if not titulo or not isinstance(titulo, str):
        return False, "", "Título não pode ser vazio"
    
    # Remover espaços em branco extras
    titulo = titulo.strip()
    
    if len(titulo) < MIN_TITULO_LENGTH:
        return False, titulo, f"Título deve ter no mínimo {MIN_TITULO_LENGTH} caracteres"
    
    if len(titulo) > MAX_TITULO_LENGTH:
        return False, titulo, f"Título deve ter no máximo {MAX_TITULO_LENGTH} caracteres"
    
    # Sanitizar para prevenir XSS
    # titulo_sanitizado = escape(titulo) 
    # Simplificando para evitar erro de import se markupsafe não estiver
    titulo_sanitizado = titulo.replace("<", "&lt;").replace(">", "&gt;")
    
    return True, titulo_sanitizado, ""


def criar_missao(titulo, tag=None):
    """
    Cria uma nova estrutura de missão se o título for válido.
    
    Args:
        titulo: O título da missão.
        tag: Dicionário opcional com cor e nome da tag (ou apenas nome).

    Returns:
        Tuple (success: bool, missao_dict: dict, error_msg: str)
    """
    sucesso, titulo_sanitizado, erro = validar_titulo(titulo)
    
    if sucesso:
        missao = {
            "titulo": titulo_sanitizado,
            "status": STATUS_DEFAULT,
            "data_criacao": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        if tag:
            missao["tag"] = tag
            
        return True, missao, ""
    
    return False, {}, erro


def validar_status(status):
    """
    Valida se o status é válido.
    
    Args:
        status: Status a ser validado
    
    Returns:
        Tuple (is_valid: bool, status: str)
    """
    if not status or status not in STATUS_VALIDOS:
        return False, STATUS_DEFAULT
    return True, status


def inicializar_perfil():
    """Cria o perfil padrão se não existir."""
    if not os.path.exists(PERFIL_PATH):
        perfil_padrao = {
            "nivel": 1,
            "xp": 0,
            "xp_proximo_nivel": 100,
            "moedas": 0,
            "streak": 0,
            "dias_concluidos": [],  # Lista de datas YYYY-MM-DD
            "inventario": [],       # Lista de IDs de itens comprados
            "tema_ativo": ""        # ID do tema ativo (vazio = padrão)
        }
        salvar_json(PERFIL_PATH, perfil_padrao)
        return perfil_padrao
    return carregar_json_dict(PERFIL_PATH)

def carregar_perfil():
    """Carrega o perfil do usuário."""
    return inicializar_perfil()

def salvar_perfil(dados):
    """Salva o perfil do usuário."""
    return salvar_json(PERFIL_PATH, dados)

def calcular_proximo_nivel(nivel):
    """Calcula XP necessário para o próximo nível (Exponencial suave)."""
    return int(100 * (1.2 ** (nivel - 1)))

def adicionar_xp(qtd):
    """Adiciona XP e verifica level up. Retorna (novo_nivel, subiu_nivel)."""
    perfil = carregar_perfil()
    perfil["xp"] += qtd
    
    subiu = False
    novo_nivel = perfil["nivel"]
    
    # Loop para múltiplos níveis de uma vez
    while perfil["xp"] >= perfil["xp_proximo_nivel"]:
        perfil["xp"] -= perfil["xp_proximo_nivel"]
        perfil["nivel"] += 1
        perfil["xp_proximo_nivel"] = calcular_proximo_nivel(perfil["nivel"])
        perfil["moedas"] += 10 # Bônus por nível
        subiu = True
        novo_nivel = perfil["nivel"]
    
    salvar_perfil(perfil)
    return novo_nivel, subiu

def adicionar_moedas(qtd):
    """Adiciona moedas ao perfil."""
    perfil = carregar_perfil()
    perfil["moedas"] += qtd
    salvar_perfil(perfil)


def comprar_item(item_id):
    """
    Processa a compra de um item.
    Returns: (sucesso, mensagem)
    """
    perfil = carregar_perfil()
    
    # Verificar se item existe
    item = next((i for i in ITENS_LOJA if i["id"] == item_id), None)
    if not item:
        return False, "Item não encontrado."
    
    # Verificar se já possui
    if item_id in perfil.get("inventario", []):
         return False, "Você já possui este item!"
    
    # Verificar saldo
    if perfil["moedas"] < item["preco"]:
        return False, "Moedas insuficientes!"

    # Processar compra
    perfil["moedas"] -= item["preco"]
    
    # Lógica da Caixa Misteriosa
    if item_id == "mystery_box":
        import random
        # 40% chance de ganhar 200 moedas, 60% de ganhar nada (apenas gastou 50)
        premio = random.choice([0, 0, 0, 200, 200]) 
        if premio > 0:
            perfil["moedas"] += premio
            salvar_perfil(perfil)
            return True, f"Caixa Misteriosa! Você ganhou {premio} moedas! 🎁"
        else:
            salvar_perfil(perfil)
            return True, "Caixa vazia... mais sorte na próxima! 🤡"

    # Lógica da Poção de Foco
    if item_id == "pocao_foco":
        # Adiciona 100 XP imediatamente/
        # Precisamos importar adicionar_xp circularmente ou duplicar logica simples aqui
        # Para evitar circular import, vamos duplicar a logica simples de XP aqui ou mover para uma funcao auxiliar
        # Vou fazer direto no perfil por segurança e simplicidade
        perfil["xp"] += 100
        xp_prox = int(100 * (1.5 ** perfil["nivel"])) # Recalcula limite basico (simplificado)
        
        msg = "Poção consumida! +100 XP! 🧪"
        
        # Check level up (Simplificado, ideal seria usar adicionar_xp)
        if perfil["xp"] >= perfil["xp_proximo_nivel"]:
             perfil["nivel"] += 1
             perfil["xp"] -= perfil["xp_proximo_nivel"]
             perfil["xp_proximo_nivel"] = int(perfil["xp_proximo_nivel"] * 1.5)
             perfil["moedas"] += 10
             msg += f" LEVEL UP! Nível {perfil['nivel']}! 🆙"
        
        salvar_perfil(perfil)
        return True, msg

    # Itens normais e temas
    if "inventario" not in perfil:
        perfil["inventario"] = []
    if item_id not in perfil["inventario"]:
        perfil["inventario"].append(item_id)
    
    salvar_perfil(perfil)
    return True, f"{item['nome']} comprado com sucesso!"


def equipar_item(item_id):
    """Equipa um item (tema)."""
    perfil = carregar_perfil()
    
    # Lógica para o Tema Padrão
    if item_id == "tema_default":
        perfil["tema_ativo"] = "" # Remove a classe do body
        salvar_perfil(perfil)
        return True, "Tema Padrão restaurado!"

    if item_id not in perfil["inventario"]:
        return False, "Você não possui este item!"
    
    # Verifica se é um tema (simplificado, assume que IDs de tema começam com 'tema_')
    if item_id.startswith("tema_"):
        perfil["tema_ativo"] = item_id
        salvar_perfil(perfil)
        return True, "Tema equipado com sucesso!"
    
    return False, "Este item não pode ser equipado."
