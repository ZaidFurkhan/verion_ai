"""Quick standalone test - run with: python test_db.py"""
import asyncio, ssl, os
from dotenv import load_dotenv

load_dotenv(override=True)

async def main():
    import asyncpg
    url = os.getenv("DATABASE_URL", "")
    # Strip the sqlalchemy driver prefix and query params for raw asyncpg
    url = url.replace("postgresql+asyncpg://", "postgresql://").split("?")[0]
    print(f"Connecting to: {url.split('@')[1]}")  # hide credentials

    ssl_ctx = ssl.create_default_context()
    try:
        conn = await asyncio.wait_for(
            asyncpg.connect(url, ssl=ssl_ctx, timeout=30),
            timeout=35
        )
        version = await conn.fetchval("SELECT version()")
        print(f"✅ Connected! PostgreSQL: {version[:40]}")
        await conn.close()
    except asyncio.TimeoutError:
        print("❌ TIMEOUT — Port 5432 is likely blocked by your firewall or ISP.")
        print("   Fix: Use Neon's connection string with port 5432 on a different network,")
        print("   or switch to psycopg2 via HTTPS proxy.")
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {e}")

asyncio.run(main())
