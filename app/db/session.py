# Placeholder for SQLAlchemy/SQLModel engine and session setup
from typing import Optional

engine = None  # set when DB chosen
SessionLocal: Optional[object] = None

async def get_session():
    # yield async session when configured
    yield None
