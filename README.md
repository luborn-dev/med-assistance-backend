# Sistema de Prontuários Médicos com IA

Este projeto é um backend desenvolvido com FastAPI para um aplicativo que integra Inteligência Artificial para transformar a maneira como os prontuários médicos são atualizados e como o histórico clínico dos pacientes é acessado. O sistema permite que a documentação dos procedimentos médicos seja atualizada em tempo real, com a IA transcrevendo as observações verbais do médico durante a consulta.

## Descrição do Produto

O projeto visa resolver problemas na atualização e no acesso aos prontuários médicos, utilizando a tecnologia de inteligência artificial para transcrever verbalmente as observações dos médicos e atualizar o prontuário dos pacientes em tempo real. Isso não apenas acelera o processo de atualização mas também aumenta a precisão e a eficiência da documentação médica.

## Tecnologias Utilizadas

- **FastAPI**: Utilizado para criar APIs de alta performance que são fáceis de desenvolver, escalar e manter.
- **Python**: Linguagem de programação escolhida devido à sua simplicidade e eficácia, além de ser amplamente usada em aplicações de inteligência artificial.

## Configuração do Projeto

### Pré-requisitos

Antes de iniciar, você precisará de Python instalado em sua máquina. Também é recomendável usar um ambiente virtual Python para instalar as dependências.

### Instalação

Clone o repositório para a sua máquina local:

```bash
git clone URL_DO_REPOSITORIO
```

Navegue até o diretório docs projeto e instale as dependências:

```bash
cd NOME_DO_DIRETORIO
pip install -r requirements.txt
```

### Executando a aplicação

Para iniciar o servidor, execute:

```bash
uvicorn main:app --reload
```

A opção `--reload` faz com que o servidor reinicie automaticamente sempre que mudanças no código são detectadas.

## Documentação da API

Após iniciar a aplicação, você pode acessar a documentação interativa gerada pelo FastAPI em `http://127.0.0.1:8000/docs`. Isso permitirá que você veja todos os endpoints disponíveis e interaja com a API diretamente pelo navegador.

```
med-assist-backend
├─ .git
│  ├─ COMMIT_EDITMSG
│  ├─ FETCH_HEAD
│  ├─ HEAD
│  ├─ branches
│  ├─ config
│  ├─ description
│  ├─ hooks
│  │  ├─ applypatch-msg.sample
│  │  ├─ commit-msg.sample
│  │  ├─ fsmonitor-watchman.sample
│  │  ├─ post-update.sample
│  │  ├─ pre-applypatch.sample
│  │  ├─ pre-commit.sample
│  │  ├─ pre-merge-commit.sample
│  │  ├─ pre-push.sample
│  │  ├─ pre-rebase.sample
│  │  ├─ pre-receive.sample
│  │  ├─ prepare-commit-msg.sample
│  │  ├─ push-to-checkout.sample
│  │  └─ update.sample
│  ├─ index
│  ├─ info
│  │  └─ exclude
│  ├─ logs
│  │  ├─ HEAD
│  │  └─ refs
│  │     ├─ heads
│  │     │  └─ main
│  │     └─ remotes
│  │        └─ origin
│  │           └─ main
│  ├─ objects
│  │  ├─ 0d
│  │  │  └─ ff5754fecab92d6f54491d1aaaf8fb0dd522f0
│  │  ├─ 15
│  │  │  └─ 0d68111440b6a6f4734bbc5367f1fc8b29eab8
│  │  ├─ 1b
│  │  │  └─ 44b4c7c500a873e0e7aeeb2b4e99d622f40832
│  │  ├─ 60
│  │  │  └─ a7ba87bfe4a1df1aefe6130dad4e72e0f50e15
│  │  ├─ 68
│  │  │  └─ bc17f9ff2104a9d7b6777058bb4c343ca72609
│  │  ├─ 85
│  │  │  └─ 91024dc3c333b66374bfc3ff684cd6b990de43
│  │  ├─ c6
│  │  │  └─ 78fe707291436cc17f572323d4935c347305e1
│  │  ├─ e6
│  │  │  └─ 9de29bb2d1d6434b8b29ae775ad8c2e48c5391
│  │  ├─ fc
│  │  │  └─ 2cbe8947627b3fab626eeaaf378312120b706e
│  │  ├─ info
│  │  └─ pack
│  └─ refs
│     ├─ heads
│     │  └─ main
│     ├─ remotes
│     │  └─ origin
│     │     └─ main
│     └─ tags
├─ .gitignore
├─ README.md
├─ app
│  ├─ __init__.py
│  ├─ config
│  │  └─ database.py
│  ├─ main.py
│  ├─ models
│  │  └─ medico_model.py
│  ├─ routers
│  │  ├─ gravacoes.py
│  │  ├─ medicos.py
│  │  └─ mock.py
│  ├─ services
│  │  ├─ gravacoes_service.py
│  │  └─ medicos_service.py
│  └─ utils
├─ requirements.txt
├─ run.sh
└─ tests
   ├─ __init__.py
   ├─ test_db.py
   └─ test_main.py

```