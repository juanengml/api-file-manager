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

# Alvo para limpar containers e imagens
clean:
	docker compose -f $(DOCKER_COMPOSE_FILE) down -v --remove-orphans
	docker image prune -af
format:
	python3 -m black .
check:
	python3 -m pytest
# Alvo padrão
.DEFAULT_GOAL := up

# Ajuda
help:
	@echo "Uso do Makefile:"
	@echo ""
	@echo "  make up         - Construir e iniciar os serviços."
	@echo "  make down       - Parar e remover os serviços."
	@echo "  make build      - Construir as imagens dos serviços."
	@echo "  make logs       - Visualizar os logs dos serviços."
	@echo "  make clean      - Limpar containers e imagens do projeto."
	@echo "  make format     - Formata o codigo usando black"
	@echo ""
	@echo "Certifique-se de ajustar a variável DOCKER_COMPOSE_FILE conforme necessário."
	@echo ""

# Alvo para manipular serviços de armazenamento
storage:
	docker compose -f $(DOCKER_COMPOSE_FILE) up -d minio

database:
	docker compose -f $(DOCKER_COMPOSE_FILE) up -d redis

