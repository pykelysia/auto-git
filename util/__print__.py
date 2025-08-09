def print_success(message: str):
    print(f"[success] {message}")

def print_error(message: str):
    print(f"[error]   {message}")

def print_start(message: str):
    print(f"[start]   {message}")

def print_end(message: str):
    print(f"[end]     {message}")

def print_warning(message: str):
    print(f"[warning] {message}")

def print_info(message: str):
    print(f"[info]    {message}")

if __name__ == "__main__":
    print_success("Hello World")
    print_error("Error")
    print_start("Start")
    print_end("End")
    print_warning("Warning")
    print_info("Info")