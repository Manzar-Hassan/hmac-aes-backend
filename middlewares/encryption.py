import json
import hashlib
import hmac
import base64
from Crypto.Cipher import AES
from django.http import JsonResponse


# AES and HMAC keys
AES_KEY = b"thisisaverysecretkey1234567890!!"
IV = b"1234567890123456"
HMAC_KEY = b"my_super_secret_hmac_key"


def decrypt_aes(encrypted_data):
    """Decrypt AES-256 CBC encrypted data"""
    try:
        # Decode base64
        encrypted_bytes = base64.b64decode(encrypted_data)

        # Create cipher
        cipher = AES.new(AES_KEY, AES.MODE_CBC, IV)

        # Decrypt
        decrypted_bytes = cipher.decrypt(encrypted_bytes)

        # Remove padding and convert to string
        decrypted_str = decrypted_bytes.decode().strip()

        # Parse JSON
        return json.loads(decrypted_str)
    except Exception as e:
        raise Exception(f"Decryption failed: {str(e)}")


def verify_hmac(data, received_hmac):
    """Verify HMAC signature"""
    expected_hmac = hmac.new(HMAC_KEY, data.encode('utf-8'), hashlib.sha256).hexdigest()

    print("Expected HMAC: ", expected_hmac)

    return hmac.compare_digest(expected_hmac, received_hmac)


class AESMiddleware:
    """Middleware to decrypt AES-encrypted requests and verify HMAC"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == "GET":
            received_hmac = request.headers.get("X-HMAC")

            if not received_hmac:
                return JsonResponse({"error": "Missing HMAC header"}, status=400)

            # Use request.path instead of get_full_path() for consistent HMAC
            url_path = request.path.rstrip("/")

            print("URL Path: ", url_path)
            print("Received HMAC: ", received_hmac)

            if not verify_hmac(url_path, received_hmac):
                return JsonResponse({"error": "Invalid HMAC signature"}, status=403)

        elif request.content_type == "application/json":
            try:
                request_data = json.loads(request.body)
                encrypted_data = request_data.get("data")
                received_hmac = request_data.get("hmac")

                if not encrypted_data or not received_hmac:
                    return JsonResponse({"error": "Missing encrypted data or HMAC"}, status=400)

                if not verify_hmac(encrypted_data, received_hmac):
                    return JsonResponse({"error": "Invalid HMAC signature"}, status=403)

                decrypted_data = decrypt_aes(encrypted_data)
                request.decoded_body = decrypted_data

            except Exception as e:
                return JsonResponse({"error": "Decryption failed", "message": str(e)}, status=400)

        return self.get_response(request)
