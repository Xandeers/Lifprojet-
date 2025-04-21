from bcrypt import checkpw, hashpw, gensalt

def hash_password(raw_password : str) -> str:
    return hashpw(raw_password.encode("utf-8"), gensalt()).decode(
        "utf-8"
    )

def check_password(password1: str, password2: str) -> bool:
    return checkpw(password1.encode("utf-8"), password2.encode("utf-8"))