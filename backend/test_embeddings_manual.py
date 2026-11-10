
from dotenv import load_dotenv

load_dotenv()

from app.services.embeddings import generate_embeddings


texts = [
    "Machine learning is a subset of artificial intelligence.",
    "Neural networks can learn complex patterns."
]

embeddings = generate_embeddings(texts)

print("Number of embeddings:", len(embeddings))
print("Dimensions per embedding:", len(embeddings[0]))
print("First five values:", embeddings[0][:5])
