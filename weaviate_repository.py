import logging

import database

logger = logging.getLogger(__name__)


def create_weaviate_schema(class_name: str):
    existing_classes = [cls["class"] for cls in database.weaviate_client.schema.get()["classes"]]

    if class_name not in existing_classes:
        database.weaviate_client.schema.create_class({
            "class": class_name,
            "vectorizer": "none",
            "properties": [
                {"name": "arxiv_id", "dataType": ["string"]},
                {"name": "text", "dataType": ["text"]},
            ]
        })


def drop_weaviate_class(class_name: str):
    if class_name in [cls["class"] for cls in database.weaviate_client.schema.get()["classes"]]:
        database.weaviate_client.schema.delete_class(class_name)


def paper_exists(class_name, arxiv_id):
    return database.weaviate_client.query.get(class_name, ["arxiv_id"]).with_where({
        "path": ["arxiv_id"],
        "operator": "Equal",
        "valueString": arxiv_id
    }).with_limit(1).do()


def create(arxiv_id, chunk, class_name, vector, uuid_str):
    database.weaviate_client.data_object.create(
        data_object={
            "arxiv_id": arxiv_id,
            "text": chunk
        },
        class_name=class_name,
        vector=vector,
        uuid=uuid_str
    )


def chunk_exists(uuid_str: str, class_name: str) -> bool:
    try:
        obj = database.weaviate_client.data_object.get_by_id(
            uuid=uuid_str,
            class_name=class_name
        )
        return obj is not None
    except Exception as e:
        logger.error(f"Error checking chunk existence for UUID {uuid_str} in class {class_name}: {e}")
        return False
