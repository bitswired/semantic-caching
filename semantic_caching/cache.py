import itertools as it
import os
from contextlib import contextmanager
from pathlib import Path
from typing import Literal

import openai
from dotenv import load_dotenv
from gptcache import cache
from gptcache.adapter import openai
from gptcache.embedding import Onnx, OpenAI
from gptcache.manager import CacheBase, VectorBase, get_data_manager
from gptcache.similarity_evaluation.distance import SearchDistanceEvaluation

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


class CacheEvaluator:
    def __init__(self):
        self.onnx = Onnx()
        self.openai = OpenAI()
        self.data_manager_onnx = get_data_manager(
            CacheBase("sqlite", sql_url="sqlite:///cache/sqlite-onnx.db"),
            VectorBase(
                "faiss",
                dimension=self.onnx.dimension,
                index_path="cache/faiss-onnx.index",
            ),
        )
        self.data_manager_openai = get_data_manager(
            CacheBase("sqlite", sql_url="sqlite:///cache/sqlite-openai.db"),
            VectorBase(
                "faiss",
                dimension=self.openai.dimension,
                index_path="cache/faiss-openai.index",
            ),
        )
        cache.set_openai_key()

    def reset(self):
        self.clear()
        self.__init__()

    def clear(self):
        paths = it.chain(Path("cache").glob("*.index"), Path("cache").glob("*.db"))
        for path in paths:
            path.unlink()

    @contextmanager
    def use_cache(self, mode: Literal["onnx", "openai"]):
        match (mode):
            case "onnx":
                cache.init(
                    embedding_func=self.onnx.to_embeddings,
                    data_manager=self.data_manager_onnx,
                    similarity_evaluation=SearchDistanceEvaluation(),
                )
            case "openai":
                cache.init(
                    embedding_func=self.openai.to_embeddings,
                    data_manager=self.data_manager_openai,
                    similarity_evaluation=SearchDistanceEvaluation(),
                )
        try:
            yield
        finally:
            pass
            # clear_cache()

    def add_to_cache(self, query: str):
        embedding = cache.embedding_func(query)
        cache.data_manager.save(query, "", embedding)

    def query(self, q: str):
        embedding = cache.embedding_func(q)
        res = cache.data_manager.search(embedding, top_k=10)
        data = [
            (cache.data_manager.get_scalar_data(x).question, x[0])
            for x in res
            if cache.data_manager.get_scalar_data(x) is not None
        ]
        return data
