# FuryCelula - Sistema de Gerenciamento de Missões

> Task Manager moderno e eficiente para organização de tarefas pessoais e projetos.

## 📝 Sobre o Projeto

**FuryCelula** é um sistema web de gerenciamento de tarefas (to-do list) desenvolvido em Flask, com foco em simplicidade, segurança e eficiência. O projeto oferece uma interface intuitiva para criação, edição, exclusão e acompanhamento de missões com diferentes status.

## ✨ Funcionalidades

- ✅ **CRUD Completo**: Criar, visualizar, editar e excluir missões
- 📈 **Dashboard com Métricas**: Visualização de progresso com estatísticas em tempo real
- 🔍 **Filtros por Status**: Filtrar missões por abertas, em andamento e concluídas
- 📝 **Histórico de Ações**: Log completo de todas as operações realizadas
- 🔄 **Reordenar Missões**: Mover tarefas para cima/baixo para priorização
- 🎨 **Interface Dark Mode**: Design moderno com tema escuro
- 🔒 **Segurança**: Validação de entrada e proteção XSS

## 💻 Tecnologias Utilizadas

- **Backend**: Python 3.x + Flask
- **Frontend**: HTML5, CSS3 (com variáveis CSS), Jinja2
- **Persistência**: JSON (arquivos locais)
- **Segurança**: MarkupSafe para sanitização XSS
- **Build**: PyInstaller (para executável standalone)

## 🛠️ Estrutura do Projeto

```
furycelula/
├── app.py                 # Aplicação Flask principal
├── config.py              # Configurações e constantes
├── utils.py               # Funções utilitárias e validação
├── data/
│   ├── missoes.json       # Armazenamento de missões
│   └── historico.json     # Log de ações
├── templates/
│   ├── base.html          # Template base
│   ├── index.html         # Página inicial
│   ├── dashboard.html     # Dashboard com métricas
│   ├── missoes.html       # Lista de missões
│   ├── editar.html        # Formulário de edição
│   └── historico.html     # Visualização do histórico
└── static/
    └── style.css          # Estilos da aplicação
```

## 🚀 Como Executar

### Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

### Instalação

1. **Clone o repositório:**
```bash
git clone https://github.com/orlei-droid/furycelula.git
cd furycelula
```

2. **Instale as dependências:**
```bash
pip install flask markupsafe
```

3. **Execute a aplicação:**
```bash
python app.py
```

4. **Acesse no navegador:**
```
http://localhost:5000
```

## 📖 Como Usar

### Criar uma Missão
1. Acesse a página "Missões" ou "Dashboard"
2. Digite o título da missão no campo de texto
3. Clique em "Adicionar"

### Gerenciar Missões
- **Iniciar**: Muda o status para "em andamento"
- **Concluir**: Marca a missão como "concluída"
- **Editar**: Permite alterar o título
- **Apagar**: Remove a missão permanentemente
- **Mover**: Setas para reordenar as missões

### Visualizar Dashboard
- Total de missões
- Missões concluídas
- Missões em aberto
- Percentual de conclusão

## 🔒 Segurança e Melhorias

### Implementações de Segurança
- ✅ Validação de entrada de dados
- ✅ Sanitização XSS com `markupsafe.escape()`
- ✅ Tratamento de erros robusto
- ✅ Backup automático de dados
- ✅ Rotação de logs (limite: 1000 entradas)

### Configurações (config.py)
```python
MAX_TITULO_LENGTH = 255      # Tamanho máximo do título
MIN_TITULO_LENGTH = 3        # Tamanho mínimo do título
MAX_HISTORICO_ENTRIES = 1000 # Limite de entradas no histórico
```

## 📚 API de Rotas

| Rota | Método | Descrição |
|------|--------|------------|
| `/` | GET | Página inicial |
| `/dashboard` | GET, POST | Dashboard com métricas |
| `/missoes` | GET, POST | Lista de missões |
| `/concluir/<int:i>` | GET | Concluir missão |
| `/editar/<int:i>` | GET, POST | Editar missão |
| `/apagar/<int:i>` | GET | Excluir missão |
| `/iniciar/<int:i>` | GET | Iniciar missão |
| `/mover/<int:i>/<direcao>` | GET | Reordenar missões |
| `/historico` | GET | Visualizar histórico |

## 👥 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto é de código aberto e disponível para uso pessoal e educacional.

## 📧 Contato

**Autor**: orlei-droid  
**GitHub**: [@orlei-droid](https://github.com/orlei-droid)

---

**Desenvolvido com ❤️ por orlei-droid**
