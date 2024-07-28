from setuptools import setup, find_packages

setup(
    name="ragnarok",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "pydantic",
        "numpy",
        # other core dependencies
    ],
    extras_require={
        "openai": ["openai"],
        "sentence_transformers": ["sentence-transformers"],
        "ollama": ["ollama"],
        "milvus": ["pymilvus"],
        "weaviate": ["weaviate-client"],
        "pinecone": ["pinecone-client"],
        "qdrant": ["qdrant-client"],
        "all": [
            "openai",
            "sentence-transformers",
            "ollama",
            "pymilvus",
            "weaviate-client",
            "pinecone-client",
            "qdrant-client",
        ],
    },
    python_requires=">=3.7",
)