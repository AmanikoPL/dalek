import os
from dotenv import load_dotenv

load_dotenv()

project_settings = {
    "title": "Tech Store Parser",
    "version": "1.0",
    "description": "FastAPI application with asyncpg and SQLAlchemy technologies",
}

class JWTTokenSettings:
    """Class containing main settings for JWT token creation."""
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "default_secret_key")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

class ParserSettings:
    """Class containing settings for web parsers."""
    SELENIUM_DRIVER_PATH: str = os.getenv("SELENIUM_DRIVER_PATH", "chromedriver")
    PARSER_TIMEOUT: int = int(os.getenv("PARSER_TIMEOUT", 10))
    PARSER_USER_AGENT: str = os.getenv(
        "PARSER_USER_AGENT",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    )

class TestDBSettings:
    """Class containing main settings for connecting to the test database."""
    DB_USER: str = "postgres"
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "admin")
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_NAME: str = "db_test_api"
    DATABASE_URL: str = (
        f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

class ProdDBSettings:
    """Class containing main settings for connecting to the production database."""
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: str = os.getenv("DB_PORT")
    DB_NAME: str = os.getenv("DB_NAME")
    
    DATABASE_URL: str = (
        f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    jwt_token_settings = JWTTokenSettings()
    parser_settings = ParserSettings()
    test_db_settings = TestDBSettings()

if __name__ == "__main__":
    prod_db_settings = ProdDBSettings()
    print("Project Title:", project_settings["title"])
    print("Database Connection URL:", prod_db_settings.DATABASE_URL)
    print("JWT Algorithm:", prod_db_settings.jwt_token_settings.JWT_ALGORITHM)
    print("Selenium Driver Path:", prod_db_settings.parser_settings.SELENIUM_DRIVER_PATH)
