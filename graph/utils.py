import re


def clean_string_for_graph(string: str) -> str:
    return re.sub(r'[^\w\s]', '', string.lower().strip()).replace(" ", "_")
