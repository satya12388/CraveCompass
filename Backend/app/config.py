from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GROQ_API_KEY: str
    LARGE_VISION_MODEL: str
    SMALL_LLM_MODEL: str
    TAVILY_API_KEY: str
    class Config:
        env_file = ".env"


settings = Settings()