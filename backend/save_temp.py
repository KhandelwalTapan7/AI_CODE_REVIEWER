def save_temp_code(code):
    temp_path = "temp_user_code.py"
    with open(temp_path, "w") as f:
        f.write(code)
    return temp_path
