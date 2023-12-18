import boto3
from PIL import Image
from io import BytesIO
import json

class Storage(object):
    def __init__(self, 
                 uri='http://miniio:9000', 
                 access_key='minio_access_key', 
                 secret_key='minio_secret_key'):
        self.uri = uri
        self.access_key = access_key
        self.secret_key = secret_key
        self.s3 = boto3.client(
            's3',
            endpoint_url=self.uri,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key
        )

    def create_bucket(self, bucket):
        # Verificar se o bucket existe e, se não existir, criar
        existing_buckets = [b['Name'] for b in self.s3.list_buckets()['Buckets']]
        if bucket not in existing_buckets:
            self.s3.create_bucket(Bucket=bucket)
            bucket_policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": "*",
                        "Action": "s3:GetObject",
                        "Resource": f"arn:aws:s3:::{bucket}/*"
                    }
                ]
            }

            bucket_policy_json = json.dumps(bucket_policy)
            self.s3.put_bucket_policy(Bucket=bucket, Policy=bucket_policy_json)

    def upload(self, bucket, file_local, file_target):
        # Verificar se o bucket existe e, se não existir, criar
        self.create_bucket(bucket)
        print(file_local, bucket, file_target)
        # Fazer o upload do arquivo
        self.s3.upload_file(file_local, bucket, file_target)

    def list_objects(self, bucket):
        # Listar objetos no bucket
        response = self.s3.list_objects(Bucket=bucket)
        return [obj['Key'] for obj in response.get('Contents', [])]
            


    def delete_bucket(self, bucket):
        # Listar objetos no bucket e excluí-los
        response = self.s3.list_objects(Bucket=bucket)
        for obj in response.get('Contents', []):
            object_key = obj['Key']
            self.s3.delete_object(Bucket=bucket, Key=object_key)

        # Agora que todos os objetos foram excluídos, você pode excluir o bucket
        self.s3.delete_bucket(Bucket=bucket)

    def get_image_bucket(self, bucket, image_path):
        try:
            # Verifique se o bucket existe
            existing_buckets = [b['Name'] for b in self.s3.list_buckets()['Buckets']]
            if bucket not in existing_buckets:
                return None, "Bucket não encontrado"

            # Obtenha a imagem do S3
            image_bytes = self.s3.get_object(Bucket=bucket, Key=image_path).get('Body').read()

            # Carregue a imagem usando o Pillow (PIL)
            image = BytesIO(image_bytes)
            return image, "Sucesso"
        except Exception as e:
            return None, str(e)
        

# Exemplo de uso:
if __name__ == "__main__":
    s3_storage = Storage(uri='http://minio:9000', access_key='minio_access_key', secret_key='minio_secret_key')
    s3_storage.upload('mybucket', 'local_file.txt', 'remote_file.txt')
    s3_storage.list_objects('mybucket')
    s3_storage.delete_bucket('mybucket')
