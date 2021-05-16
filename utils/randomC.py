import random


def RandomColorGenerator() -> str:
    hex_nu = random.randint(0, 16777215)
    return format(hex_nu, 'x')
