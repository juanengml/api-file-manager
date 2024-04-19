import pytest
import requests


# URL base da sua API (substitua localhost pelo endereço correto se estiver em outro lugar)
base_url = "http://localhost:5000"
id_device = "123"
BASE_URL = "http://localhost:5000"


def test_release():
    # Simula um arquivo a ser enviado
    file_data = {"file": open("tests/app.log", "rb")}
    response = requests.post(f"{BASE_URL}/release", files=file_data)
    assert response.status_code == 201


def test_release_listar():
    response = requests.get(f"{BASE_URL}/release")
    assert response.status_code == 200
    # Verifica se a resposta contém uma lista de releases
    assert "releases" in response.json()


def test_cadastrar():
    # Simula um arquivo de imagem
    image = {"image": open("images/image-1.png", "rb")}
    response = requests.post(f"{BASE_URL}/cadastrar", files=image)
    assert response.status_code == 201


def test_listar():
    response = requests.get(f"{BASE_URL}/listar")
    assert response.status_code == 200
    # Verifica se a resposta contém uma lista de imagens
    assert "imagens" in response.json()


def test_send_log():
    url = f"{base_url}/log_device/{id_device}"
    log_data = {
        "app": {
            "timestamp": 1706016312,
            "fwVersion": "v1.3.0",
            "hwVersion": "v1.0.0",
            "serialNumber": "0x1231237894579834857938457",
        },
        "accelerometer": {
            "enable": True,
            "error": 0,
            "x": 10,
            "y": 10,
            "z": 10,
            "vibrationDetect": True,
        },
        "infra_red": {"enable": True, "error": 0, "humanDetect": False},
        "battery": {
            "enable": True,
            "error": 0,
            "accumulatedCapacity": 2000,
            "temperature": 25,
            "voltage": 330,
            "batteryStatus": 10,
            "batteryAlert": 100,
            "current": 100,
            "scaled_r": 10,
            "measured_z": 20,
            "internalTemperature": 30,
            "stateOfHealth": 3,
            "designCapacity": 5,
            "cal_count": 10,
            "cal_current": 100,
            "cal_voltage": 1000,
            "cal_temperature": 10000,
        },
        "camera": {"error": 0},
        "memory": {"error": 0, "sizeMemory": 134217728, "usedMemory": 1024},
        "wifi": {
            "device": "DA16200",
            "sdk": "3.2.8.0",
            "version": "FRTOS-GEN01-01-f017bfdf51-006558",
            "dhcp": True,
            "ip_address": "192.168.1.19",
            "netmask": "255.255.255.0",
            "gateway": "192.168.1.1",
            "dns": "192.168.1.1",
            "dns2": "192.168.1.2",
            "sntp": "pool.ntp.org",
            "sntp2": "1.pool.ntp.org",
            "ssid": "@MyNetwork",
            "mac": "AA:BB:CC:DD:EE:FF",
        },
    }
    response = requests.post(url, json=log_data)
    assert response.status_code == 200


# Teste para obter configuração de um dispositivo
def test_get_config():
    url = f"{base_url}/get_config/{id_device}"
    print(url)
    response = requests.get(url)
    assert response.status_code == 200
    assert "status" in response.json()  # Verifica se a resposta contém a chave 'app'


def test_ping():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    }
    response = requests.get(f"{base_url}/", headers=headers)
    assert response.status_code == 200
