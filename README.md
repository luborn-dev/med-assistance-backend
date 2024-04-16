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

Navegue até o diretório do projeto e instale as dependências:

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
