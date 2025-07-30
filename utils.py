import itertools

def stripText(input: str):
    cleaned_lines = list(
        itertools.dropwhile(lambda x: not x.strip(), input.splitlines())
    )
    return "\n".join(cleaned_lines)