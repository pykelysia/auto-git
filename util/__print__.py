def print_success(message: str):
    print(f"[success] {message}")

def print_error(message: str):
    print(f"[error]   {message}")

if __name__ == "__main__":
    print_success("Hello World")
    print_error("Error")