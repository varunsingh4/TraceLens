from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """All knobs for milestone 1 live here so you can change them without hunting the code."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+psycopg2://tracelens:tracelens@localhost:5433/tracelens"
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "tracelens_chunks"
    # MiniLM is small, local, and 384-dimensional. Swap later without changing retrieval logic.
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    chunk_size: int = 500
    chunk_overlap: int = 80


settings = Settings()
