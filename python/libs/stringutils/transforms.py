"""String transformation utilities."""


def capitalize_words(text: str) -> str:
    return " ".join(word.capitalize() for word in text.split())


def reverse_string(text: str) -> str:
    return text[::-1]


def snake_to_camel(text: str) -> str:
    parts = text.split("_")
    return parts[0] + "".join(word.capitalize() for word in parts[1:])


def camel_to_snake(text: str) -> str:
    result = [text[0].lower()]
    for char in text[1:]:
        if char.isupper():
            result.append("_")
            result.append(char.lower())
        else:
            result.append(char)
    return "".join(result)


def truncate(text: str, max_length: int, suffix: str = "...") -> str:
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix
