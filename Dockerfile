# Base Image com Python
FROM python:3.9-slim

# Define o diretório de trabalho no container
WORKDIR /flaskapp

# Copia os arquivos requirements.txt para o container
COPY requirements.txt .

# Instala as dependências da aplicação
RUN pip install --no-cache-dir -r requirements.txt

# Copia todos os arquivos do diretório atual para o container
COPY . .

# Expõe a porta que o Flask usará
EXPOSE 5000

# Comando para iniciar a aplicação
CMD ["python", "Docker.py"]
