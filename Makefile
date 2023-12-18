# Nome da imagem Docker
DOCKER_IMAGE_NAME = api-file-manager

# Porta em que a aplicação Flask irá rodar no host
HOST_PORT = 5000
# ENV = /home/juannascimento/.env

# Comando para construir a imagem Docker
build:
	docker build -t $(DOCKER_IMAGE_NAME) .

# Comando para executar o contêiner Docker
run:
	docker run --rm --name $(DOCKER_IMAGE_NAME) -p $(HOST_PORT):$(HOST_PORT) $(DOCKER_IMAGE_NAME)

# Comando para purgar (remover) o contêiner Docker
purge:
	docker stop $$(docker ps -q --filter ancestor=$(DOCKER_IMAGE_NAME)) || true
	docker rm $$(docker ps -a -q --filter ancestor=$(DOCKER_IMAGE_NAME)) || true

# Alvo padrão
.DEFAULT_GOAL := run

# Ajuda
help:
	@echo "Uso do Makefile:"
	@echo ""
	@echo "  make build     - Construir a imagem Docker da API Flask."
	@echo "  make run       - Executar o contêiner Docker com a API Flask."
	@echo "  make purge     - Parar e remover o contêiner Docker."
	@echo ""
	@echo "Certifique-se de ajustar as variáveis DOCKER_IMAGE_NAME e HOST_PORT conforme necessário."
