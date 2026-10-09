import os

# Reads Render's DATABASE_URL first, defaulting to 'db' only for local docker-compose
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://ecommerce_user:password@db:5432/ecommerce")