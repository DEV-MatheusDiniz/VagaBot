# Usa uma imagem base do Python
FROM python:3.12-slim


# Instala dependências
RUN apt-get update && apt-get install -y --no-install-recommends \
    apt-utils locales firefox-esr wget \
    && echo "pt_BR.UTF-8 UTF-8" >> /etc/locale.gen \
    && echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen \
    && locale-gen pt_BR.UTF-8 en_US.UTF-8 \
    && rm -rf /var/lib/apt/lists/*

# # Baixa e instala o geckodriver
# RUN GECKODRIVER_VERSION=0.33.0 && \
#     wget -q "https://github.com/mozilla/geckodriver/releases/download/v$GECKODRIVER_VERSION/geckodriver-v$GECKODRIVER_VERSION-linux64.tar.gz" -O /tmp/geckodriver.tar.gz && \
#     tar -zxf /tmp/geckodriver.tar.gz -C /usr/local/bin && \
#     rm /tmp/geckodriver.tar.gz && \
#     chmod +x /usr/local/bin/geckodriver

# Instala as dependências Python
RUN pip install --no-cache-dir poetry

# Copia todo o conteúdo do projeto
COPY . .

# Instala as dependências do projeto
RUN poetry install --no-root

# Inicia o script
CMD ["poetry", "run", "python", "main.py"]
