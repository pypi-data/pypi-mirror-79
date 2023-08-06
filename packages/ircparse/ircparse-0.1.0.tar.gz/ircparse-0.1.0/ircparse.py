from typing import Dict, List, Literal, Optional

from pydantic import BaseModel


class Message(BaseModel):
    tags: Dict[str, Optional[str]] = {}
    prefix: Optional[str] = None
    params: List[str]


def parse(text: str):
    tags = {}

    if text.startswith("@"):
        tags_text, text = text[1:].split(maxsplit=1)
        for tag_text in tags_text.split(";"):
            if "=" in tag_text:
                key, val = tag_text.split("=", maxsplit=1)
                tags[key] = val
            else:
                key = tag_text
                tags[key] = None

    prefix = None

    if text.startswith(":"):
        prefix, text = text[1:].split(maxsplit=1)

    words = text.split()
    maxsplit = -1
    for i, word in enumerate(words):
        if word.startswith(":"):
            maxsplit = i
            break

    params = text.split(maxsplit=maxsplit)
    if params and params[-1].startswith(":"):
        params[-1] = params[-1][1:]

    return Message(tags=tags, prefix=prefix, params=params)


def unparse(msg: Message):
    text = []

    if msg.tags:
        text.append(
            "@"
            + ";".join(
                f"{key}={val}" if val is not None else key
                for key, val in msg.tags.items()
            )
        )

    if msg.prefix is not None:
        text.append(f":{msg.prefix}")

    trail = False
    for param in msg.params:
        if param.startswith(":") or len(param.split()) > 1 or len(param) == 0:
            assert not trail, "only one parameter can be trail"
            trail = True
            text.append(f":{param}")
        else:
            text.append(param)

    return " ".join(text)
