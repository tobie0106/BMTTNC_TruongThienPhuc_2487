from flask import Flask, request, jsonify
from cipher.caesar import CaesarCipher
# from cipher.playfair import PlayFairCipher
# from cipher.transposition import TranspositionCipher
from cipher.railfence import RailFenceCipher
app = Flask(__name__)

# ==============================
# INIT CIPHER
# ==============================

caesar_cipher = CaesarCipher()
# playfair_cipher = PlayFairCipher()
# transposition_cipher = TranspositionCipher()
railfence_cipher = RailFenceCipher()

# ==============================
# CAESAR API
# ==============================

@app.route("/api/caesar/encrypt", methods=["POST"])
def caesar_encrypt():
    data = request.json

    plain_text = data['plain_text']
    key = int(data['key'])

    encrypted_text = caesar_cipher.encrypt_text(plain_text, key)

    return jsonify({
        "encrypted_message": encrypted_text
    })


@app.route("/api/caesar/decrypt", methods=["POST"])
def caesar_decrypt():
    data = request.json

    cipher_text = data['cipher_text']
    key = int(data['key'])

    decrypted_text = caesar_cipher.decrypt_text(cipher_text, key)

    return jsonify({
        "decrypted_message": decrypted_text
    })


# ==============================
# PLAYFAIR API
# ==============================

@app.route('/api/playfair/creatematrix', methods=['POST'])
def playfair_creatematrix():

    data = request.get_json()
    key = data.get("key")

    playfair_matrix = playfair_cipher.create_key(key)

    return jsonify({
        "playfair_matrix": playfair_matrix
    })


@app.route('/api/playfair/encrypt', methods=['POST'])
def playfair_encrypt():

    data = request.get_json()

    plain_text = data.get("plain_text")
    key = data.get("key")

    playfair_matrix = playfair_cipher.create_key(key)

    encrypted_text = playfair_cipher.playfair_encrypt(
        plain_text,
        playfair_matrix
    )

    return jsonify({
        "encrypted_text": encrypted_text
    })


@app.route('/api/playfair/decrypt', methods=['POST'])
def playfair_decrypt():

    data = request.get_json()

    cipher_text = data.get("cipher_text")
    key = data.get("key")

    playfair_matrix = playfair_cipher.create_key(key)

    decrypted_text = playfair_cipher.playfair_decrypt(
        cipher_text,
        playfair_matrix
    )

    return jsonify({
        "decrypted_text": decrypted_text
    })


# ==============================
# TRANSPOSITION API
# ==============================

@app.route('/api/transposition/encrypt', methods=['POST'])
def transposition_encrypt():

    data = request.get_json()

    plain_text = data.get('plain_text')
    key = int(data.get('key'))

    encrypted_text = transposition_cipher.encrypt(
        plain_text,
        key
    )

    return jsonify({
        "encrypted_text": encrypted_text
    })


@app.route('/api/transposition/decrypt', methods=['POST'])
def transposition_decrypt():

    data = request.get_json()

    cipher_text = data.get('cipher_text')
    key = int(data.get('key'))

    decrypted_text = transposition_cipher.decrypt(
        cipher_text,
        key
    )

    return jsonify({
        "decrypted_text": decrypted_text
    })

# ==============================
# RAILFENCE API
# ==============================

@app.route('/api/railfence/encrypt', methods=['POST'])
def railfence_encrypt():

    data = request.get_json()

    plain_text = data['plain_text']
    key = int(data['key'])

    encrypted_text = railfence_cipher.rail_fence_encrypt(
        plain_text,
        key
    )

    return jsonify({
        "encrypted_text": encrypted_text
    })


@app.route('/api/railfence/decrypt', methods=['POST'])
def railfence_decrypt():

    data = request.get_json()

    cipher_text = data['cipher_text']
    key = int(data['key'])

    decrypted_text = railfence_cipher.rail_fence_decrypt(
        cipher_text,
        key
    )

    return jsonify({
        "decrypted_text": decrypted_text
    })
    
   
# ==============================
# MAIN
# ==============================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)