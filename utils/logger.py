import time


def log(message):
    """
    Print timestamped log message.
    """

    now = time.strftime("%H:%M:%S")

    print(f"[{now}] {message}")