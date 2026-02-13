"""Aplicação Flask - FuryCelula V-42

Aplicação de gerenciamento de missões com gamificação.
"""
import random
import os
from flask import Flask, render_template, request, redirect, url_for, flash

# Importar configurações e utilitários
from config import (
    MISSOES_PATH,
    HISTORICO_PATH,
    PERFIL_PATH,
    FLASK_DEBUG,
    FLASK_SECRET_KEY,
    ITENS_LOJA
)
from utils import (
    carregar_json,
    salvar_json,
    salvar_log,
    criar_missao,
    validar_titulo,
    carregar_perfil,
    salvar_perfil,
    adicionar_xp,
    adicionar_moedas,
    comprar_item,
    equipar_item
)

app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY


@app.route("/")
def index():
    """Página inicial."""
    return render_template("index.html")


@app.context_processor
def inject_perfil():
    """Injeta o perfil em todos os templates para acessar o tema ativo."""
    p = carregar_perfil()
    # print(f"DEBUG: Tema Ativo = {p.get('tema_ativo')}")
    return dict(perfil=p)


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    """Dashboard com métricas e adição de missões."""
    missoes = carregar_json(MISSOES_PATH)
    perfil = carregar_perfil()
    
    if request.method == "POST":
        titulo = request.form.get("missao", "").strip()
        tag_nome = request.form.get("tag_nome")
        tag_cor = request.form.get("tag_cor")
        
        tag = None
        if tag_nome and tag_cor:
             tag = {"nome": tag_nome, "cor": tag_cor}

        # Usar função de validação do utils
        sucesso, nova_missao, erro = criar_missao(titulo, tag)
        
        if sucesso:
            missoes.append(nova_missao)
            if salvar_json(MISSOES_PATH, missoes):
                salvar_log("Criou missão", titulo)
                novo_nivel, subiu = adicionar_xp(10)
                msg = "Missão criada (+10 XP)!"
                if subiu:
                    msg += f" SUBIU DE NÍVEL! {novo_nivel}!"
                flash(msg, "success")
            else:
                flash("Erro ao salvar missão", "error")
        else:
            flash(erro, "error")
        
        return redirect(url_for("dashboard"))
    
    # Calcular métricas
    total = len(missoes)
    concluidas = len([m for m in missoes if m.get("status") == "concluída"])
    abertas = total - concluidas
    percentual = round((concluidas / total) * 100, 1) if total > 0 else 0
    
    return render_template(
        "dashboard.html",
        missoes=missoes,
        total=total,
        concluidas=concluidas,
        abertas=abertas,
        percentual=percentual,
        perfil=perfil
    )


@app.route("/missoes", methods=["GET", "POST"])
def missoes():
    """Lista de missões com filtros."""
    todas_missoes = carregar_json(MISSOES_PATH)
    status_filtro = request.args.get("status")
    
    # Aplicar filtro se especificado
    if status_filtro:
        missoes_filtradas = [m for m in todas_missoes if m.get("status") == status_filtro]
    else:
        missoes_filtradas = todas_missoes
    
    if request.method == "POST":
        titulo = request.form.get("nova_missao", "").strip()
        tag_nome = request.form.get("tag_nome")
        tag_cor = request.form.get("tag_cor")
        
        tag = None
        if tag_nome and tag_cor:
            tag = {"nome": tag_nome, "cor": tag_cor}
        
        # Usar função de validação
        sucesso, nova_missao, erro = criar_missao(titulo, tag)
        
        if sucesso:
            todas_missoes.append(nova_missao)
            if salvar_json(MISSOES_PATH, todas_missoes):
                salvar_log("Criou missão", titulo)
                novo_nivel, subiu = adicionar_xp(10)
                msg = "Missão criada (+10 XP)!"
                if subiu:
                    msg += f" SUBIU DE NÍVEL! {novo_nivel}!"
                flash(msg, "success")
            else:
                flash("Erro ao salvar missão", "error")
        else:
            flash(erro, "error")
        
        return redirect(url_for("missoes", status=status_filtro))
    
    return render_template(
        "missoes.html",
        missoes=missoes_filtradas,
        status_filtro=status_filtro or ""
    )



@app.route("/registrar/<int:i>")
def registrar_progresso(i):
    """Registra progresso em uma missão sem concluí-la."""
    from datetime import datetime
    
    missoes = carregar_json(MISSOES_PATH)
    
    if 0 <= i < len(missoes):
        missao = missoes[i]
        
        # Criar array de registros se não existir
        if "registros" not in missao:
            missao["registros"] = []
        
        # Adicionar novo registro com timestamp
        timestamp = datetime.now().isoformat()
        missao["registros"].append({"data": timestamp})
        
        if salvar_json(MISSOES_PATH, missoes):
            salvar_log("Registrou progresso", missao["titulo"])
            novo_nivel, subiu = adicionar_xp(5)
            msg = f"Progresso registrado! (+5 XP) Total: {len(missao['registros'])}x"
            if subiu:
                msg += f" SUBIU DE NÍVEL! {novo_nivel}!"
            flash(msg, "success")
        else:
            flash("Erro ao registrar progresso", "error")
    else:
        flash("Missão não encontrada", "error")
    
    return redirect(url_for("dashboard"))


@app.route("/concluir/<int:i>")
def concluir_missao(i):
    """Marca uma missão como concluída."""
    missoes = carregar_json(MISSOES_PATH)
    
    if 0 <= i < len(missoes):
        missao = missoes[i]
        if missao["status"] != "concluída":
            missao["status"] = "concluída"
            
            if salvar_json(MISSOES_PATH, missoes):
                salvar_log("Concluiu missão", missao["titulo"])
                novo_nivel, subiu = adicionar_xp(50)
                adicionar_moedas(5)
                msg = "Missão concluída (+50 XP, +5 Moedas)!"
                if subiu:
                    msg += f" SUBIU DE NÍVEL! {novo_nivel}!"
                flash(msg, "success")
            else:
                flash("Erro ao atualizar missão", "error")
        else:
            flash("Missão já concluída", "info")
    else:
        flash("Missão não encontrada", "error")
    
    return redirect(url_for("dashboard"))


@app.route("/editar/<int:i>", methods=["GET", "POST"])
def editar_missao(i):
    """Edita o título de uma missão."""
    missoes = carregar_json(MISSOES_PATH)
    
    # Verificar se o índice é válido
    if not (0 <= i < len(missoes)):
        flash("Missão não encontrada", "error")
        return redirect(url_for("missoes"))
    
    if request.method == "POST":
        novo_titulo = request.form.get("novo_titulo", "").strip()
        tag_nome = request.form.get("tag_nome")
        tag_cor = request.form.get("tag_cor")
        
        # Validar novo título
        is_valid, titulo_sanitizado, erro = validar_titulo(novo_titulo)
        
        if is_valid:
            titulo_antigo = missoes[i]["titulo"]
            missoes[i]["titulo"] = titulo_sanitizado
            
            # Atualizar tag
            if tag_nome and tag_cor:
                missoes[i]["tag"] = {"nome": tag_nome, "cor": tag_cor}
            else:
                # Remover tag se "Sem Tag" foi selecionado
                if "tag" in missoes[i]:
                    del missoes[i]["tag"]
            
            if salvar_json(MISSOES_PATH, missoes):
                salvar_log("Editou missão", f"{titulo_antigo} → {titulo_sanitizado}")
                flash("Missão editada com sucesso!", "success")
            else:
                flash("Erro ao salvar alterações", "error")
            
            return redirect(url_for("missoes"))
        else:
            flash(erro, "error")
    
    perfil = carregar_perfil()
    return render_template("editar.html", missao=missoes[i], perfil=perfil, i=i)


@app.route("/apagar/<int:i>")
def apagar_missao(i):
    """Exclui uma missão."""
    missoes = carregar_json(MISSOES_PATH)
    
    if 0 <= i < len(missoes):
        titulo = missoes[i]["titulo"]
        del missoes[i]
        
        if salvar_json(MISSOES_PATH, missoes):
            salvar_log("Excluiu missão", titulo)
            flash("Missão excluída", "success")
        else:
            flash("Erro ao excluir missão", "error")
    else:
        flash("Missão não encontrada", "error")
    
    return redirect(url_for("missoes"))


@app.route("/mover/<int:i>/<direcao>")
def mover_missao(i, direcao):
    """Reordena missões (mover para cima ou baixo)."""
    missoes = carregar_json(MISSOES_PATH)
    
    if direcao == "cima" and i > 0:
        missoes[i], missoes[i - 1] = missoes[i - 1], missoes[i]
        salvar_json(MISSOES_PATH, missoes)
    elif direcao == "baixo" and i < len(missoes) - 1:
        missoes[i], missoes[i + 1] = missoes[i + 1], missoes[i]
        salvar_json(MISSOES_PATH, missoes)
    else:
        flash("Não é possível mover nessa direção", "warning")
    
    return redirect(url_for("missoes"))


@app.route("/iniciar/<int:i>")
def iniciar_missao(i):
    """Marca missão como em andamento."""
    missoes = carregar_json(MISSOES_PATH)
    
    if 0 <= i < len(missoes):
        missoes[i]["status"] = "em_andamento"
        if salvar_json(MISSOES_PATH, missoes):
            salvar_log("Iniciou missão", missoes[i]["titulo"])
            flash("Missão iniciada!", "success")
        else:
            flash("Erro ao atualizar missão", "error")
    else:
        flash("Missão não encontrada", "error")
    
    return redirect(url_for("missoes"))


@app.route("/tags/nova", methods=["POST"])
def nova_tag():
    """Cria uma nova tag para as missões."""
    nome = request.form.get("nome_tag", "").strip()
    cor = request.form.get("cor_tag", "#000000")
    
    if not nome:
        flash("Nome da tag é obrigatório!", "error")
        return redirect(url_for("dashboard"))
        
    perfil = carregar_perfil()
    if "tags" not in perfil:
        perfil["tags"] = []
    
    # Verificar duplicidade
    if any(t["nome"] == nome for t in perfil["tags"]):
         flash("Tag já existe!", "error")
         return redirect(url_for("dashboard"))

    perfil["tags"].append({"nome": nome, "cor": cor})
    salvar_perfil(perfil)
    flash(f"Tag '{nome}' criada!", "success")
    return redirect(url_for("dashboard"))


@app.route("/tags/deletar/<nome>")
def deletar_tag(nome):
    """Remove uma tag do perfil e de todas as missões."""
    perfil = carregar_perfil()
    missoes = carregar_json(MISSOES_PATH)
    
    if "tags" in perfil:
        # Filtrar removendo a tag com o nome correspondente
        original_len = len(perfil["tags"])
        perfil["tags"] = [t for t in perfil["tags"] if t["nome"] != nome]
        
        if len(perfil["tags"]) < original_len:
            # Remover a tag de todas as missões
            missoes_afetadas = 0
            for missao in missoes:
                if "tag" in missao and missao["tag"]["nome"] == nome:
                    del missao["tag"]
                    missoes_afetadas += 1
            
            salvar_perfil(perfil)
            salvar_json(MISSOES_PATH, missoes)
            
            if missoes_afetadas > 0:
                flash(f"Tag '{nome}' removida de {missoes_afetadas} missão(ões).", "success")
            else:
                flash(f"Tag '{nome}' removida.", "success")
        else:
            flash("Tag não encontrada.", "error")
            
    return redirect(url_for("configuracoes"))


@app.route("/configuracoes")
def configuracoes():
    """Página de configurações."""
    perfil = carregar_perfil()
    return render_template("configuracoes.html", perfil=perfil)


@app.route("/tags/deletar-todas", methods=["POST"])
def deletar_todas_tags():
    """Deleta todas as tags do perfil."""
    perfil = carregar_perfil()
    if "tags" in perfil:
        count = len(perfil["tags"])
        perfil["tags"] = []
        salvar_perfil(perfil)
        flash(f"{count} tag(s) deletada(s).", "success")
    else:
        flash("Nenhuma tag para deletar.", "error")
    return redirect(url_for("configuracoes"))


@app.route("/reset/progresso", methods=["POST"])
def resetar_progresso():
    """Reseta apenas XP, nível e moedas."""
    perfil = carregar_perfil()
    perfil["nivel"] = 1
    perfil["xp"] = 0
    perfil["xp_proximo_nivel"] = 100
    perfil["moedas"] = 0
    salvar_perfil(perfil)
    salvar_log("Resetou progresso", "Nível, XP e Moedas")
    flash("Progresso resetado! Você voltou ao nível 1.", "success")
    return redirect(url_for("configuracoes"))


@app.route("/reset/tudo", methods=["POST"])
def resetar_tudo():
    """Reseta missões e histórico, mas mantém progresso (XP, Nível, Moedas)."""
    # Resetar missões
    salvar_json(MISSOES_PATH, [])
    
    # Resetar histórico
    salvar_json(HISTORICO_PATH, [])
    
    salvar_log("Resetou missões e histórico", "Manteve progresso")
    flash("🔄 Missões e histórico deletados! Seu progresso foi mantido.", "success")
    return redirect(url_for("configuracoes"))


@app.route("/reset/deletar-tudo", methods=["POST"])
def deletar_tudo():
    """Deleta ABSOLUTAMENTE TUDO e recomeça do zero."""
    # Resetar missões
    salvar_json(MISSOES_PATH, [])
    
    # Resetar histórico
    salvar_json(HISTORICO_PATH, [])
    
    # Resetar perfil para padrão
    from utils import inicializar_perfil
    if os.path.exists(PERFIL_PATH):
        os.remove(PERFIL_PATH)
    inicializar_perfil()
    
    flash("💀 TUDO foi deletado! Começando do zero absoluto.", "success")
    return redirect(url_for("dashboard"))


@app.route("/historico")
def historico():
    """Visualiza histórico de ações."""
    logs = carregar_json(HISTORICO_PATH)
    return render_template("historico.html", logs=logs)


@app.route("/loja")
def loja():
    """Exibe a loja de itens."""
    perfil = carregar_perfil()
    return render_template("loja.html", itens=ITENS_LOJA, perfil=perfil)


@app.route("/loja/comprar/<item_id>")
def comprar(item_id):
    """Rota para comprar um item."""
    sucesso, msg = comprar_item(item_id)
    if sucesso:
        flash(msg, "success")
        salvar_log("Comprou item", item_id)
    else:
        flash(msg, "error")
    return redirect(url_for("loja"))


@app.route("/loja/equipar/<item_id>")
def equipar(item_id):
    """Rota para equipar um tema."""
    sucesso, msg = equipar_item(item_id)
    if sucesso:
        flash(msg, "success")
        # salvar_log("Equipou tema", item_id) # Removido a pedido
    else:
        flash(msg, "error")
    return redirect(url_for("loja"))


if __name__ == "__main__":
    app.run(debug=FLASK_DEBUG)
