import hashlib
import uuid

from pathlib import Path

from langchain_core.documents import (
    Document
)

from langchain_community.vectorstores import (
    FAISS
)

from app.config import get_settings

from app.services.chunking import (
    chunk_text
)

from app.services.embeddings import (
    get_embeddings
)

from app.services.parsers import (
    SUPPORTED,
    parse_file
)

from app.services.vector_store import (
    VectorStoreManager
)


class IngestionService:

    def __init__(self):

        self.settings = get_settings()

        self.stores = (
            VectorStoreManager()
        )

    def _document_id(
        self,
        path: Path
    ) -> str:

        digest = hashlib.sha256(
            path.read_bytes()
        ).hexdigest()[:12]

        return f"doc-{digest}"

    def ingest(
        self,
        files: list[tuple[str, bytes]]
    ):

        if not files:

            raise ValueError(
                "At least one document "
                "is required"
            )

        collection_id = (
            uuid.uuid4().hex[:16]
        )

        collection_dir = (
            self.settings.upload_dir
            / collection_id
        )

        collection_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        all_documents = []

        document_infos = []

        for filename, content in files:

            suffix = (
                Path(filename)
                .suffix
                .lower()
            )

            if suffix not in SUPPORTED:

                raise ValueError(
                    f"Unsupported file "
                    f"'{filename}'. "
                    f"Use PDF, TXT, or Markdown."
                )

            if not content:

                raise ValueError(
                    f"File '{filename}' "
                    f"is empty."
                )

            safe_name = Path(
                filename
            ).name

            path = (
                collection_dir
                / safe_name
            )

            path.write_bytes(
                content
            )

            text = parse_file(
                path
            )

            if not text:

                raise ValueError(
                    f"No extractable text "
                    f"found in '{filename}'."
                )

            document_id = (
                self._document_id(path)
            )

            chunks = chunk_text(

                text,

                chunk_size=(
                    self.settings.chunk_size
                ),

                overlap=(
                    self.settings.chunk_overlap
                ),
            )

            if not chunks:

                raise ValueError(
                    f"No chunks were created "
                    f"for '{filename}'."
                )

            for chunk in chunks:

                all_documents.append(

                    Document(

                        page_content=(
                            chunk.text
                        ),

                        metadata={

                            "document_id":
                                document_id,

                            "filename":
                                safe_name,

                            "file_type":
                                suffix,

                            "chunk_id":
                                chunk.chunk_id,

                            "start":
                                chunk.start,

                            "end":
                                chunk.end,
                        },
                    )
                )

            document_infos.append(

                {
                    "document_id":
                        document_id,

                    "filename":
                        safe_name,

                    "file_type":
                        suffix,

                    "chunks":
                        len(chunks),
                }
            )

        vectorstore = (
            FAISS.from_documents(

                all_documents,

                get_embeddings()
            )
        )

        metadata = {

            "collection_id":
                collection_id,

            "documents":
                document_infos,

            "total_chunks":
                len(all_documents),
        }

        self.stores.save(

            collection_id,

            vectorstore,

            metadata,
        )

        return (
            collection_id,
            document_infos
        )
