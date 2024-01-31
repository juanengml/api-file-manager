from lodge import logger
from flask import Flask, request, jsonify, send_file
from lmodel.storage import Storage
from create_db import createDB
import sqlite3
import redis
import json

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configuração do Redis
redis_host = 'redis'
redis_port = 6379
redis_db = 0

redis_conn = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)



# Rota para cadastrar uma imagem
s3_storage = Storage()
@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    data = request.form

    if 'image' not in request.files:
        logger.error('Nenhuma imagem encontrada no formulário')
        return 'Nenhuma imagem encontrada no formulário', 400
    image = request.files['image']
    image_name = image.filename
    if not image.filename.endswith(('.png', '.jpg', '.jpeg')):
        logger.error('Formato de imagem não suportado')
        return jsonify({'error': 'Formato de imagem não suportado'}), 400
    
    image_local = f'uploads/images/{image_name}_{image.filename}'
    bucket = "bucket"
    target_image = f"folder/{image.filename}"

    image.save(image_local)
    logger.info(f'Imagem salva localmente: {image_local}')
    
    s3_storage.upload(bucket, image_local, target_image)
    logger.info('Imagem carregada para o S3')
    
    return 'Imagem cadastrada com sucesso!', 201
    
# Rota para listar todas as imagens enviadas
@app.route('/listar')
def listar():
    try:
        bucket = "bucket"
        objects = s3_storage.list_objects(bucket)
        object = [f"http://localhost:5000/get_image/bucket/{i}" for i in objects]
        return {'imagens': object}, 200
    except Exception as err:
        logger.error(f'Erro ao listar imagens: {err}')
        return 'Erro ao listar imagens', 500

# Rota para obter uma imagem específica
@app.route('/get_image/<bucket>/<path:image_path>')
def get_image(bucket, image_path):
    try:
        image, status = s3_storage.get_image_bucket(bucket, image_path)

        # Verifique se a imagem foi obtida com sucesso
        if image is not None:
            # Use send_file para enviar a imagem como resposta
            return send_file(image, mimetype='image/jpeg')
        else:
            return f"Erro: {status}", 404
    except Exception as err:
        logger.error(f'Erro ao obter imagem: {err}')
        return 'Erro ao obter imagem', 500

# Rota para obter a configuração de um dispositivo
@app.route('/get_config/<id_device>', methods=['GET'])
def get_config(id_device):
    try:
        # Consulta ao Redis para obter a configuração
        config_json = redis_conn.get(id_device)

        if config_json:
            # Decodifica os dados JSON do Redis
            config = json.loads(config_json)
            return jsonify(config), 200
        else:
            return "Device not found", 404
    except Exception as err:
        logger.error(f'Erro ao obter configuração do dispositivo: {err}')
        return 'Erro ao obter configuração do dispositivo', 500


# Rota para receber os logs do dispositivo
@app.route('/log_device/<id_device>', methods=['POST'])
def log_device(id_device):
    try:
        log_data = request.json

        # Salvar os dados de log no Redis
        redis_conn.set(id_device, json.dumps(log_data))


        logger.info(f'Dados de log recebidos do dispositivo {id_device}: {log_data}')
        return "Log received", 200
    except Exception as err:
        logger.error(f'Erro ao receber logs do dispositivo {id_device}: {err}')
        return 'Erro ao receber logs do dispositivo', 500


@app.route('/', methods=['GET'])
def status():
    return {"status":"work"}, 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
