# Use a imagem base do Python 3.8
FROM python:3.8

# Define o diretório de trabalho no container
WORKDIR /app

RUN apt update
RUN apt-get install libgl1-mesa-glx -y


# Copie os arquivos do diretório local para o diretório de trabalho no container
COPY . /app


# Instale as dependências da sua API Flask
RUN pip install -r requirements.txt

# Expõe a porta em que a sua aplicação Flask irá rodar (ajuste conforme necessário)
EXPOSE 5001

# Comando para executar a sua aplicação Flask
CMD ["python", "api.py"]
