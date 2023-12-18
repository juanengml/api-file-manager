# API Simples com Flask e MinIO

## Descrição
Esta é uma API simples criada com Flask para cadastrar, listar e obter imagens. As imagens são armazenadas no MinIO, um serviço de armazenamento de objetos.


## Subindo Mini IO
```bash
docker run -p 9000:9000 --name miniio -e "MINIO_ACCESS_KEY=minio_access_key" -e "MINIO_SECRET_KEY=minio_secret_key" minio/minio server /data   
```

## Para Subir A API

```bash
make build 
make run

```
## Rotas

### Cadastrar uma imagem
Endpoint: `/cadastrar` (método POST)

Cadastra uma nova imagem no MinIO.

**Exemplo de uso:**
```bash
curl -X POST -F "image=@/caminho/do/seu/arquivo/imagem.jpg" http://localhost:5000/cadastrar

```

### Listar Imagens
Endpoint: `/listar` (método GET)

Cadastra uma nova imagem no MinIO.

**Exemplo de uso:**
```bash
curl http://localhost:5000/listar

```

### Obter uma imagem específica

Endpoint: `/get_image/<bucket>/<path:image_path>` (método GET)

Obtém uma imagem específica do MinIO.

**Exemplo de uso:**

```bash
curl -O http://localhost:5000/get_image/seu-bucket/folder/nome-da-imagem.jpg
```
