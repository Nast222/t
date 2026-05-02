import random
import string

def generate_password(length, use_digits, use_letters, use_special):
    if length < 4 or length > 128:
        raise ValueError("Длина пароля должна быть от 4 до 128 символов.")

    chars = ''
    if use_digits:
        chars += string.digits
    if use_letters:
        chars += string.ascii_letters
    if use_special:
        chars += string.punctuation

    if not chars:
        raise ValueError("Выберите хотя бы один тип символов.")

    return ''.join(random.choices(chars, k=length))
