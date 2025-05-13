# Vaga Bot

Tem o objetivo de coletar vagas e enviar via chat automaticamente.

## Dependências
- Python v3.12.3
- Docker v26.1.3
- Docker compose v2.29.4
- Poetry v1.8.5

## Execução do Projeto
```shell
# Instalar dependências do projeto
poetry install

# Ativar ambiente virtual
poetry shell

# Executar projeto
python main.py

# Se quiser executar o projeto para testar sem usar o schedule, execute:
python teste.py
```

## Execução do Projeto (Docker)
```shell
docker compose up
```
