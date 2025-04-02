import json
import base64
import hashlib
import hmac
import requests
from Crypto.Cipher import AES


AES_KEY = b"thisisaverysecretkey1234567890!!"
IV = b"1234567890123456"
HMAC_KEY = b"my_super_secret_hmac_key"


def encrypt_aes(data):
    """Encrypt AES-256 CBC"""
    cipher = AES.new(AES_KEY, AES.MODE_CBC, IV)
    padded_data = json.dumps(data).ljust(16 * ((len(json.dumps(data)) // 16) + 1))
    encrypted_bytes = cipher.encrypt(padded_data.encode())
    return base64.b64encode(encrypted_bytes).decode()


def generate_hmac(data):
    """Generate HMAC SHA-256"""
    return hmac.new(HMAC_KEY, data.encode(), hashlib.sha256).hexdigest()


def test_get_request():
    url = "http://127.0.0.1:8000/books"
    hmac_signature = generate_hmac("/books")

    headers = {
        "X-HMAC": hmac_signature
    }
    get_response = requests.get(url, headers=headers)

    print("\n=== GET Request Test ===\n")
    print("HMAC Signature:", hmac_signature)
    print("Response:", get_response.text)


def test_post_request():
    url = "http://127.0.0.1:8000/books"
    data = {
        "title": "Test Book",
        "author": "Test Author",
        "published_date": "2025-04-01",
        "description": "A test book description"
    }

    encrypted_data = encrypt_aes(data)
    hmac_signature = generate_hmac(encrypted_data)

    headers = {"Content-Type": "application/json"}
    payload = json.dumps({"data": encrypted_data, "hmac": hmac_signature})

    post_response = requests.post(url, headers=headers, data=payload)

    print("\n=== POST Request Test ===\n")
    print("Encrypted Payload:")
    print(json.dumps({"data": encrypted_data, "hmac": hmac_signature}, indent=4))

    try:
        print("Response:", post_response.json())
    except requests.exceptions.JSONDecodeError as e:
        print("JSON Decode Error:", str(e))


if __name__ == "__main__":
    # test_get_request()
    test_post_request()
