from . import ALPHABET

class CaesarCipher:
    def __init__(self):
        self.alphabet = ALPHABET

    def _shift_char(self, letter: str, key: int, encrypt: bool = True) -> str:
        if not letter.isalpha():
            return letter

        letter = letter.upper()
        alphabet_len = len(self.alphabet)
        letter_index = self.alphabet.index(letter)

        if encrypt:
            output_index = (letter_index + key) % alphabet_len
        else:
            output_index = (letter_index - key) % alphabet_len

        return self.alphabet[output_index]


    def encrypt_text(self, text: str, key: int) -> str:
        key = key % len(self.alphabet)
        return "".join(self._shift_char(letter, key, encrypt=True) for letter in text)


    def decrypt_text(self, text: str, key: int) -> str:
        key = key % len(self.alphabet)
        return "".join(self._shift_char(letter, key, encrypt=False) for letter in text)