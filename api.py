from flask import Flask, request, jsonify, send_file
from lmodel.storage import Storage

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Rota para cadastrar uma imagem

s3_storage = Storage()


@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    data = request.form

    if 'image' not in request.files:
        return 'Nenhuma imagem encontrada no formulário', 400
    image = request.files['image']
    image_name = image.filename
    if not image.filename.endswith(('.png', '.jpg', '.jpeg')):
        return jsonify({'error': 'Formato de image não suportado'}), 400
    
    image_local = f'uploads/images/{image_name}_{image.filename}'
    bucket = "bucket"
    target_image = f"folder/{image.filename}"

    image.save(image_local)
    print(image_local)
        
    s3_storage.upload(bucket, image_local, target_image)
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
        print(err)
        return 'Erro ao listar imagens', 500

# Rota para obter uma imagem específica
@app.route('/get_image/<bucket>/<path:image_path>')
def get_image(bucket, image_path):
    
    image, status = s3_storage.get_image_bucket(bucket, image_path)

    # Verifique se a imagem foi obtida com sucesso
    if image is not None:
        # Use send_file para enviar a imagem como resposta
        return send_file(image, mimetype='image/jpeg')
    else:
        return f"Erro: {status}", 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
