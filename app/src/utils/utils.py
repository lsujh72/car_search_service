import random


def randchar(x: str, y: str) -> str:
    return chr(random.randint(ord(x), ord(y)))


def create_unique_number() -> str:
    return f"{str(random.randint(1000, 10000))}{randchar('A', 'Z')}"
