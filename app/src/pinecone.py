import os
import time
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec


load_dotenv()


def get_pinecone_client():
    """Initialize and return a Pinecone client using the API key from .env."""
    api_key = os.getenv("PINECONE_API_KEY")
    if not api_key:
        raise ValueError("PINECONE_API_KEY not found in environment variables.")
    return Pinecone(api_key=api_key)


def get_or_create_index(pc, index_name, dimension=768, cloud="aws", region="us-east-1", metric="cosine"):
    """Create a Pinecone index if it doesn't exist, and return the index object."""
    if not pc.has_index(index_name):
        pc.create_index(
            name=index_name,
            dimension=dimension,
            metric=metric,
            spec=ServerlessSpec(cloud=cloud, region=region)
        )
    return pc.Index(index_name)


def batch_upsert(index, namespace, records, batch_size=96, delay=2):
    """
    Upsert records to Pinecone index in batches.
    Each record should be a dict: {"id": str, "values": list, "metadata": dict}
    """
    for i in range(0, len(records), batch_size):
        batch = records[i:i+batch_size]
        index.upsert(vectors=batch, namespace=namespace)
        time.sleep(delay)