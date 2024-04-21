from lodge import logger
from flask import Flask, request, jsonify, send_file
from lmodel.storage import Storage
from lmodel.database import Database
from io import BytesIO

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

db = Database()
s3_storage = Storage()


@app.route("/cadastrar", methods=["POST"])
def cadastrar():
    if "image" not in request.files:
        logger.error("Nenhuma imagem encontrada no formulário")
        return {"status": "Nenhuma imagem encontrada no formulário"}, 400
    image = request.files["image"]
    image_name = image.filename
    if not image.filename.endswith((".png", ".jpg", ".jpeg")):
        logger.error("Formato de imagem não suportado")
        return jsonify({"error": "Formato de imagem não suportado"}), 400

    image_local = f"uploads/images/{image_name}"
    bucket = "bucket"
    target_image = f"folder/{image.filename}"

    image.save(image_local)
    logger.info(f"Imagem salva localmente: {image_local}")

    s3_storage.upload(bucket, image_local, target_image)
    logger.info("Imagem carregada para o S3")

    return {"status": "Imagem cadastrada com sucesso!"}, 201


@app.route("/release", methods=["POST"])
def release():
    file_release = request.files["file"]
    file_name = file_release.filename

    image_local = f"uploads/releases/{file_name}_{file_release.filename}"
    bucket = "release"
    target_image = f"release/{file_name}"

    file_release.save(image_local)
    logger.info(f"Arquivo salvo localmente: {image_local}")

    s3_storage.upload(bucket, image_local, target_image)
    logger.info("Arquivo carregada para o S3")

    return {"status": "Imagem cadastrada com sucesso!"}, 201


@app.route("/release", methods=["GET"])
def release_listar():
    try:
        bucket = "release"
        objects = s3_storage.list_objects(bucket)
        print(objects)
        object = [f"http://localhost:5000/get_release/release/{i}" for i in objects]
        return {"status": object}, 200
    except Exception as err:
        logger.error(f"Erro ao listar releases: {err}")
        return {"status": "Erro ao listar releases"}, 500


# Rota para obter uma imagem específica
@app.route("/get_release/<bucket>/<path:image_path>")
def get_release(bucket, image_path):
    try:
        release_data, status = s3_storage.get_release_bucket(bucket, image_path)

        if release_data:
            # Criar um objeto BytesIO a partir dos dados do release
            release_stream = BytesIO(release_data)
            # Enviar o arquivo do release como resposta
            return send_file(release_stream, mimetype="application/octet-stream")
        else:
            return {"status": f"Erro: {status}"}, 404
    except Exception as err:
        logger.error(f"Erro ao obter release: {err}")
        return {"status": "Erro ao obter release"}, 500


# Rota para listar todas as imagens enviadas
@app.route("/listar")
def listar():
    try:
        bucket = "bucket"
        objects = s3_storage.list_objects(bucket)
        object = [f"http://localhost:5000/get_image/bucket/{i}" for i in objects]
        return {"imagens": object}, 200
    except Exception as err:
        logger.error(f"Erro ao listar imagens: {err}")
        return {"status": "Erro ao listar imagens"}, 500


# Rota para obter uma imagem específica
@app.route("/get_image/<bucket>/<path:image_path>")
def get_image(bucket, image_path):
    try:
        image, status = s3_storage.get_image_bucket(bucket, image_path)

        if image is not None:
            return send_file(image, mimetype="image/jpeg")
        else:
            return {"status": f"Erro: {status}"}, 404
    except Exception as err:
        logger.error(f"Erro ao obter imagem: {err}")
        return {"status": "Erro ao obter imagem"}, 500


# Rota para obter a configuração de um dispositivo
@app.route("/get_config/<id_device>", methods=["GET"])
def get_config(id_device):
    try:
        logger.info(f"AQUI - {id_device}")
        config = db.select(id_device)

        if isinstance(config, str):
            return jsonify(config), 404
        else:
            return {"status": config}, 200
    except Exception as err:
        logger.error(f"Erro ao obter configuração do dispositivo: {err}")
        return {"status": "Erro ao obter configuração do dispositivo"}, 500


# Rota para receber os logs do dispositivo
@app.route("/log_device/<id_device>", methods=["POST"])
def log_device(id_device):
    try:
        log_data = request.json
        db.insert(id_device, log_data)
        logger.info(f"Dados de log recebidos do dispositivo {id_device}: {log_data}")
        return {"status": "Log received"}, 200
    except Exception as err:
        logger.error(f"Erro ao receber logs do dispositivo {id_device}: {err}")
        return {"status": f"Erro ao receber logs do dispositivo - {err}"}, 500


@app.route("/", methods=["GET"])
def status():
    return {"status": "work"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
