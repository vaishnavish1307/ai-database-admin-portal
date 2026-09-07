from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://neondb_owner:npg_Xpkg1Jmu7QhD@ep-cold-surf-axxmfyb6.c-4.us-east-2.aws.neon.tech/neondb?sslmode=require"

engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version();"))
        print("Connected successfully!")
        print(result.fetchone())

except Exception as e:
    print("Connection failed:")
    print(e)