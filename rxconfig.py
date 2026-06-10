import os
import reflex as rx

# Railway injeta DATABASE_URL com "postgres://", mas SQLAlchemy exige "postgresql://"
_db_url = os.environ.get("DATABASE_URL", "sqlite:///reflex.db")
if _db_url.startswith("postgres://"):
    _db_url = _db_url.replace("postgres://", "postgresql://", 1)

config = rx.Config(
    app_name="app",
    plugins=[
        rx.plugins.TailwindV3Plugin(),
        rx.plugins.SitemapPlugin(),
    ],
    db_url=_db_url,
    show_built_with_reflex=False,
)
