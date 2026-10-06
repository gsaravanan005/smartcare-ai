import os
from dataclasses import dataclass

@dataclass
class Settings:
    PROJECT_NAME: str = "SmartCare AI - Healthcare AI Platform"
    API_V1_STR: str = "/api"
    SECRET_KEY: str = "smartcare_ai_super_secret_jwt_key_2026_module1"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day

    BASE_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    RAW_DATA_DIR: str = os.path.join(BASE_DIR, "data", "raw")
    WORKING_DATA_DIR: str = os.path.join(BASE_DIR, "data", "working")
    PROCESSED_DATA_DIR: str = os.path.join(BASE_DIR, "data", "processed")
    ARTIFACTS_DIR: str = os.path.join(BASE_DIR, "artifacts", "module2_inputs")

    DATABASE_URL: str = f"sqlite:///{os.path.join(BASE_DIR, 'smartcare_module1.db')}"

    # MongoDB Integration Settings
    MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017/smartcare_ai")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "smartcare_ai")

    DEFAULT_TRAIN_RATIO: float = 0.70
    DEFAULT_VAL_RATIO: float = 0.15
    DEFAULT_TEST_RATIO: float = 0.15
    DEFAULT_RANDOM_SEED: int = 42

settings = Settings()
