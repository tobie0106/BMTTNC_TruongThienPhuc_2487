from flask import Flask, request, jsonify
from cipher.caesar import CaesarCipher
from cipher.vigenere import VigenereCipher
app = Flask(__name__)

# CAESAR CIPHER ALGORITHM
caesar_cipher = CaesarCipher()

@app.route("/api/caesar/encrypt", methods=["POST"])
def caesar_encrypt():
    data = request.json
    plain_text = data['plain_text']
    key = int(data['key'])
    encrypted_text = caesar_cipher.encrypt_text(plain_text, key)
    return jsonify({'encrypted_message': encrypted_text})


@app.route("/api/caesar/decrypt", methods=["POST"])
def caesar_decrypt():
    data = request.json
    cipher_text = data['cipher_text']
    key = int(data['key'])
    decrypted_text = caesar_cipher.decrypt_text(cipher_text, key)
    return jsonify({'decrypted_message': decrypted_text})

vigenere_cipher = VigenereCipher()

@app.route('/api/vigenere/encrypt', methods=['POST'])
def vigenere_encrypt():
    try:
        data = request.get_json()
        plain_text = data.get('plain_text', '')
        key = data.get('key', '')
        
        if not plain_text or not key:
            return jsonify({
                "error": "Cần cung cấp 'plain_text' và 'key'"
            }), 400
            
        encrypted_text = vigenere_cipher.vigenere_encrypt(plain_text, key)
        
        return jsonify({
            "encrypted_text": encrypted_text
        })
        
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


@app.route('/api/vigenere/decrypt', methods=['POST'])
def vigenere_decrypt():
    try:
        data = request.get_json()
        cipher_text = data.get('cipher_text', '')
        key = data.get('key', '')
        
        if not cipher_text or not key:
            return jsonify({
                "error": "Cần cung cấp 'cipher_text' và 'key'"
            }), 400
            
        decrypted_text = vigenere_cipher.vigenere_decrypt(cipher_text, key)
        
        return jsonify({
            "decrypted_text": decrypted_text
        })
        
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500
# main function
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)