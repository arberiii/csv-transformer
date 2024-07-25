import os

import openai
import pandas as pd

from embeding_storage import EmbeddingStorage

openai.api_key = os.getenv('OPENAI_API_KEY')

MODEL_SMALL = 'text-embedding-3-small'
MODEL_LARGE = 'text-embedding-3-large'

small_storage = EmbeddingStorage('embeddings_small.json')
large_storage = EmbeddingStorage('embeddings_large.json')


def get_embedding(text, engine=MODEL_SMALL):
    if engine == MODEL_SMALL:
        storage = small_storage
    else:
        storage = large_storage

    if value := storage.get(text):
        return value
    response = openai.Embedding.create(
        input=[text],
        engine=engine
    )
    value = response['data'][0]['embedding']
    storage.set(text, value)
    return value


def cosine_similarity(vec1, vec2):
    return sum(x * y for x, y in zip(vec1, vec2)) / (
            (sum(x ** 2 for x in vec1) ** 0.5) * (sum(y ** 2 for y in vec2) ** 0.5))


def find_most_similar_word(words, concept):
    concept_embedding = get_embedding(concept)
    similarities = []

    for word in words:
        word_embedding = get_embedding(word)
        similarity = cosine_similarity(concept_embedding, word_embedding)
        similarities.append((word, similarity))

    most_similar_word = max(similarities, key=lambda x: x[1])
    return most_similar_word


def get_csv_headers(df: pd.DataFrame):
    header = df.columns.tolist()
    return [col for col in header if col.strip()]
