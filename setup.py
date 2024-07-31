from setuptools import setup, find_packages

def get_requires():
    with open("requirements.txt", "r", encoding="utf-8") as f:
        file_content = f.read()
        lines = [line.strip() for line in file_content.strip().split("\n") if not line.startswith("#")]
        return lines

setup(
    name="ragnarok",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=get_requires(),
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