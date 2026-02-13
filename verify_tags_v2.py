from utils import criar_missao, carregar_perfil, salvar_perfil
import datetime

def test_tags_v2():
    print("Testing Tag System V2 (Fixes & Management)...")
    
    # 1. Criar Tag no Perfil
    perfil = carregar_perfil()
    tag_teste = {"nome": "TEST_V2", "cor": "#FF00FF"}
    
    if "tags" not in perfil:
        perfil["tags"] = []
    
    # Limpar anterior
    perfil["tags"] = [t for t in perfil["tags"] if t["nome"] != "TEST_V2"]
    perfil["tags"].append(tag_teste)
    salvar_perfil(perfil)
    print(" - Tag 'TEST_V2' criada.")

    # 2. Criar Missão com Tag (Agora deve funcionar)
    sucesso, missao, erro = criar_missao("Missão Tag V2", tag_teste)
    
    if sucesso and missao.get("tag") == tag_teste:
        print(" - SUCESSO: Missão criada com tag corretamente.")
    else:
        print(f" - FALHA: Missão não salvou tag. Erro: {erro}")
        print(f" - Dados da missão: {missao}")
        return

    # 3. Testar Deletar Tag (Simulando a lógica da rota)
    print(" - Testando exclusão...")
    perfil = carregar_perfil()
    original_len = len(perfil["tags"])
    perfil["tags"] = [t for t in perfil["tags"] if t["nome"] != "TEST_V2"]
    
    if len(perfil["tags"]) < original_len:
        salvar_perfil(perfil)
        print(" - SUCESSO: Tag 'TEST_V2' removida do perfil.")
    else:
        print(" - FALHA: Tag não foi removida.")

if __name__ == "__main__":
    test_tags_v2()
