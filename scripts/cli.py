from enum import Enum

import typer
from rich import print
from rich.panel import Panel

from semantic_caching.utils import run_and_format, use_tmp_cache

app = typer.Typer()


class CacheType(str, Enum):
    no_cache = "no_cache"
    semantic_cache = "semantic_cache"


@app.command()
def run(cache_type: CacheType):
    match (cache_type):
        case CacheType.no_cache:
            ctx = use_tmp_cache("no")
        case CacheType.semantic_cache:
            ctx = use_tmp_cache("semantic")

    with ctx as openai:
        display_group = run_and_format(openai)

        match (cache_type):
            case CacheType.no_cache:
                print(
                    Panel.fit(
                        display_group,
                        title="NO CACHE",
                        border_style="blue",
                    )
                )
            case CacheType.semantic_cache:
                print(
                    Panel.fit(
                        display_group,
                        title="Semantic Cache",
                        border_style="blue",
                    )
                )


if __name__ == "__main__":
    app()
