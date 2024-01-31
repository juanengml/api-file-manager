# Nome do arquivo Docker Compose
DOCKER_COMPOSE_FILE = docker-compose.yml

# Comando para construir e iniciar os serviços
up:
	docker compose -f $(DOCKER_COMPOSE_FILE) up -d

# Comando para parar e remover os serviços
down:
	docker compose -f $(DOCKER_COMPOSE_FILE) down

# Comando para construir as imagens
build:
	docker compose -f $(DOCKER_COMPOSE_FILE) build

# Comando para visualizar os logs dos serviços
logs:
	docker compose -f $(DOCKER_COMPOSE_FILE) logs

check:
	python3 -m pytest
# Alvo padrão
.DEFAULT_GOAL := up

# Ajuda
help:
	@echo "Uso do Makefile:"
	@echo ""
	@echo "  make up        - Construir e iniciar os serviços."
	@echo "  make down      - Parar e remover os serviços."
	@echo "  make build     - Construir as imagens dos serviços."
	@echo "  make logs      - Visualizar os logs dos serviços."
	@echo ""
	@echo "Certifique-se de ajustar a variável DOCKER_COMPOSE_FILE conforme necessário."
