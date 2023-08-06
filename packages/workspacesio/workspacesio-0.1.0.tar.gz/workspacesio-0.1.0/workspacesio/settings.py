import os

SECRET = os.environ.get("WIO_SECRET", "fast")
PUBLIC_NAME = os.environ.get("WIO_PUBLIC_NAME", "http://localhost:8100").rstrip("/")
SQLALCHEMY_DATABASE_URL = os.environ.get(
    "WIO_DATABASE_URL",
    f"postgresql://wio:workspaces@localhost:5555/wio",
)
ES_NODE_1 = os.environ.get("WIO_ELASTICSEARCH_NODE_1", "http://localhost:9200")
ES_NODES = [ES_NODE_1]
