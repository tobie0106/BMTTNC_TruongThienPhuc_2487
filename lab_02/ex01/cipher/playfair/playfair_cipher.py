class PlayFairCipher:

    def __init__(self):
        pass

    def create_key(self, key):
        key = key.upper().replace("J", "I")
        key = "".join(dict.fromkeys(key))

        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        matrix = list(key)

        for letter in alphabet:
            if letter not in matrix:
                matrix.append(letter)

        playfair_matrix = [matrix[i:i+5] for i in range(0, 25, 5)]
        return playfair_matrix

    def tach_cap_playfair(self, text):
        text = text.upper().replace("J", "I").replace(" ", "")
        result = []
        i = 0

        while i < len(text):
            a = text[i]

            if i + 1 < len(text):
                b = text[i + 1]

                if a == b:
                    result.append(a + "X")
                    i += 1
                else:
                    result.append(a + b)
                    i += 2
            else:
                result.append(a + "X")
                i += 1

        return result

    def index_letter(self, matrix, letter):
        for row in range(len(matrix)):
            for col in range(len(matrix[row])):
                if matrix[row][col] == letter:
                    return row, col

    def playfair_encrypt(self, plain_text, matrix):
        pairs = self.tach_cap_playfair(plain_text)
        encrypted_text = ""

        for pair in pairs:
            row1, col1 = self.index_letter(matrix, pair[0])
            row2, col2 = self.index_letter(matrix, pair[1])

            if row1 == row2:
                encrypted_text += matrix[row1][(col1 + 1) % 5]
                encrypted_text += matrix[row2][(col2 + 1) % 5]

            elif col1 == col2:
                encrypted_text += matrix[(row1 + 1) % 5][col1]
                encrypted_text += matrix[(row2 + 1) % 5][col2]

            else:
                encrypted_text += matrix[row1][col2]
                encrypted_text += matrix[row2][col1]

        return encrypted_text

    def playfair_decrypt(self, cipher_text, matrix):
        decrypted_text = ""

        for i in range(0, len(cipher_text), 2):
            a = cipher_text[i]
            b = cipher_text[i + 1]

            row1, col1 = self.index_letter(matrix, a)
            row2, col2 = self.index_letter(matrix, b)

            if row1 == row2:
                decrypted_text += matrix[row1][(col1 - 1) % 5]
                decrypted_text += matrix[row2][(col2 - 1) % 5]

            elif col1 == col2:
                decrypted_text += matrix[(row1 - 1) % 5][col1]
                decrypted_text += matrix[(row2 - 1) % 5][col2]

            else:
                decrypted_text += matrix[row1][col2]
                decrypted_text += matrix[row2][col1]

        # bỏ X nếu được thêm vào
        banro = ""

        for i in range(0, len(decrypted_text) - 2, 2):
            if decrypted_text[i] == decrypted_text[i + 2]:
                banro += decrypted_text[i]
            else:
                banro += decrypted_text[i] + decrypted_text[i + 1]

        if decrypted_text[-1] == "X":
            banro += decrypted_text[-2]
        else:
            banro += decrypted_text[-2] + decrypted_text[-1]

        return banro