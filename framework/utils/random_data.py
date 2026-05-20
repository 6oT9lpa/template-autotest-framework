import random


class RandomData:
    _WORDS = (
        "atlas",
        "binary",
        "cosmos",
        "delta",
        "ember",
        "forest",
        "harbor",
        "matrix",
        "orbit",
        "vector",
    )

    @staticmethod
    def readable_text(prefix: str = "Autotest") -> str:
        word = random.choice(RandomData._WORDS)
        number = random.randint(1000, 9999)
        return f"{prefix} {word} {number}"
