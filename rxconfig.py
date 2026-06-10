import os
import reflex as rx

# Railway injeta DATABASE_URL com "postgres://", mas SQLAlchemy exige "postgresql://"
_db_url = os.environ.get("DATABASE_URL", "sqlite:///reflex.db")
if _db_url.startswith("postgres://") or _db_url.startswith("postgresql://"):
    _db_url = _db_url.replace("postgres://", "postgresql://", 1)
    if "sslmode=" not in _db_url:
        _db_url += "?sslmode=require" if "?" not in _db_url else "&sslmode=require"

config = rx.Config(
    app_name="app",
    plugins=[
        rx.plugins.TailwindV3Plugin(),
        rx.plugins.SitemapPlugin(),
    ],
    db_url=_db_url,
    show_built_with_reflex=False,
)
