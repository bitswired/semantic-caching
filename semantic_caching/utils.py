import itertools as it
import os
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from gptcache.embedding import Onnx
from gptcache.manager import CacheBase, VectorBase, get_data_manager
from gptcache.similarity_evaluation.distance import SearchDistanceEvaluation
from rich.console import Group
from rich.progress import track
from rich.rule import Rule
from rich.text import Text

load_dotenv()


def format_result(question: str, answer: str, time_consuming: float):
    return Group(
        Text("🤔 Question: ", style="bold green", end=""),
        Text(question),
        Text("🤖 Answer: ", style="bold blue", end=""),
        Text(answer),
        Text("⏳ Time consuming: ", style="bold yellow", end=""),
        Text(f"{time_consuming:.2f}s"),
    )


def response_text(openai_resp):
    return openai_resp["choices"][0]["message"]["content"]


def run_and_format(openai):
    questions = [
        "what's github",
        "what's github",
        "can you explain what GitHub is",
        "can you tell me more about GitHub",
        "what is the purpose of GitHub",
    ]

    display_groups = []
    for i, question in enumerate(track(questions)):
        start_time = time.time()
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": question}],
            max_tokens=128,
        )
        display_groups.append(
            format_result(question, response_text(response), time.time() - start_time)
        )
        if i != len(questions) - 1:
            display_groups.append(Rule())

    return Group(
        *display_groups,
    )


def clear_tmp_cache():
    paths = it.chain(Path("cache").glob("*tmp.index"), Path("cache").glob("*tmp.db"))
    for path in paths:
        path.unlink()


@contextmanager
def use_tmp_cache(mode: Literal["exact", "semantic", "no"]):
    clear_tmp_cache()
    match (mode):
        case "semantic":
            from gptcache import cache
            from gptcache.adapter import openai

            openai.api_key = os.getenv("OPENAI_API_KEY")
            cache.set_openai_key()

            onnx = Onnx()
            data_manager = get_data_manager(
                CacheBase("sqlite", sql_url="sqlite:///cache/sqlite-tmp.db"),
                VectorBase(
                    "faiss",
                    dimension=onnx.dimension,
                    index_path="cache/faiss-tmp.index",
                ),
            )
            cache.init(
                embedding_func=onnx.to_embeddings,
                data_manager=data_manager,
                similarity_evaluation=SearchDistanceEvaluation(),
            )
        case "no":
            import openai

            pass

    try:
        yield openai
    finally:
        pass
        clear_tmp_cache()
