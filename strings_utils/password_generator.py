import secrets
import string

def generate_secure_password(length=12):
    """
    Generates a secure, random password.

    Args:
        length (int): The desired length of the password.

    Returns:
        str: The generated secure password.
    """
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return password

# Example usage:
password = generate_secure_password(16)
print(f"Generated password: {password}")