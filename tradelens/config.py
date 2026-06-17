import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


class Config:
    COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY", "")
    ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY", "")
    PORT = int(os.getenv("PORT", "8000"))
    HOST = os.getenv("HOST", "0.0.0.0")
    DB_PATH = os.getenv("DB_PATH", "data/tradelens.db")

    @classmethod
    def has_coingecko_pro(cls) -> bool:
        return bool(cls.COINGECKO_API_KEY)
