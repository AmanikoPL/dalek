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
    DATABASE_URL: str = os.getenv("TEST_DATABASE_URL", "postgresql+psycopg2://postgres:admin@localhost:5432/db_test_api")

class ProdDBSettings:
    """Class containing main settings for connecting to the production database."""
    DATABASE_URL: str = os.getenv("DATABASE_URL")

    jwt_token_settings = JWTTokenSettings()
    parser_settings = ParserSettings()
    test_db_settings = TestDBSettings()

if __name__ == "__main__":
    prod_db_settings = ProdDBSettings()
    print("Project Title:", project_settings["title"])
    print("Database Connection URL:", prod_db_settings.DATABASE_URL)
    print("JWT Algorithm:", prod_db_settings.jwt_token_settings.JWT_ALGORITHM)
    print("Selenium Driver Path:", prod_db_settings.parser_settings.SELENIUM_DRIVER_PATH)
