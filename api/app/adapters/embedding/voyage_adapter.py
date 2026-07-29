import voyageai

from app.adapters.embedding.base import EmbeddingClient


class VoyageEmbeddingAdapter(EmbeddingClient):

    def __init__(self, api_key: str, model: str, output_dimension: int):
        self._client = voyageai.AsyncClient(api_key=api_key)
        self._model = model
        self._output_dimension = output_dimension

    async def embed(self, texts: list[str]) -> list[list[float]]:
        result = await self._client.embed(
            texts, model=self._model, output_dimension=self._output_dimension, input_type="document"
        )
        return result.embeddings
