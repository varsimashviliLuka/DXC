from src import create_app
from src.config import TestConfig

app = create_app(TestConfig)

# app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0')