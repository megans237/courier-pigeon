import dotenv
import os

if __name__ == "__main__":
    dotenv.load_dotenv()

    SOLACE_USERNAME = os.getenv("SOLACE_USERNAME")
    print(SOLACE_USERNAME)
    DEBUG = int(os.getenv("DEBUG"))
    print(DEBUG)
    print(type(DEBUG))
