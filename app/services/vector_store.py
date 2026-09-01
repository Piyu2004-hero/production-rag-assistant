import json
from pathlib import Path

from langchain_community.vectorstores import (
    FAISS
)

from app.config import get_settings


class VectorStoreManager:

    def __init__(self):

        self.settings = get_settings()

    def collection_path(
        self,
        collection_id: str
    ) -> Path:

        return (
            self.settings.index_dir
            / collection_id
        )

    def save(
        self,
        collection_id: str,
        vectorstore: FAISS,
        metadata: dict,
    ):

        path = self.collection_path(
            collection_id
        )

        path.mkdir(
            parents=True,
            exist_ok=True
        )

        vectorstore.save_local(
            str(path)
        )

        (
            path / "metadata.json"
        ).write_text(
            json.dumps(
                metadata,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

    def exists(
        self,
        collection_id: str
    ) -> bool:

        path = self.collection_path(
            collection_id
        )

        return (
            (path / "index.faiss").exists()
            and
            (path / "index.pkl").exists()
        )

    def load(
        self,
        collection_id: str
    ) -> FAISS:

        from app.services.embeddings import (
            get_embeddings
        )

        path = self.collection_path(
            collection_id
        )

        if not self.exists(
            collection_id
        ):

            raise FileNotFoundError(
                f"Collection not found: "
                f"{collection_id}"
            )

        return FAISS.load_local(

            str(path),

            get_embeddings(),

            allow_dangerous_deserialization=True,
        )

    def metadata(
        self,
        collection_id: str
    ) -> dict:

        path = (
            self.collection_path(
                collection_id
            )
            / "metadata.json"
        )

        if not path.exists():

            return {}

        return json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )
