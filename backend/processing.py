import os

import openai
import pandas as pd

openai.api_key = os.getenv('OPENAI_API_KEY')

KV = {}

MODEL_SMALL = 'text-embedding-3-small'
MODEL_LARGE = 'text-embedding-3-large'

def get_embedding(text, engine=MODEL_SMALL):
    if text in KV:
        return KV[text]
    response = openai.Embedding.create(
        input=[text],
        engine=engine
    )
    KV[text] = response['data'][0]['embedding']
    return response['data'][0]['embedding']


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
