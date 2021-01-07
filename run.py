from app import create_app
from dotenv import load_dotenv

load_dotenv('.env')

app = create_app()

if __name__ == "__main__":
    app.secret_key=app.config.get("SECRET_KEY")
    app.run(debug=True, port=8432)
