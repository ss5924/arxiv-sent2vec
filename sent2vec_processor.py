import uuid

from weaviate.util import get_valid_uuid

import weaviate_repository
from logging_config import logger
from text_spilt import split_text


async def process_paper(doc, semaphore, class_name, batch_id, model):
    async with semaphore:
        try:
            arxiv_id = doc.get("arxiv_id")
            content = doc.get("cleaned_text", "")
            if not arxiv_id or not content.strip():
                logger.info(f"[SKIP][W{batch_id}] Invalid document - arxiv_id: {arxiv_id}")
                return

            logger.info(f"[PROCESS][W{batch_id}] Starting - arxiv_id: {arxiv_id}")

            chunks = split_text(content)
            embeddings = model.encode(chunks, batch_size=32, show_progress_bar=False)

            for i, (chunk, vector) in enumerate(zip(chunks, embeddings)):
                uuid_str = get_valid_uuid(uuid.uuid5(uuid.NAMESPACE_DNS, f"{arxiv_id}_{i}"))

                if weaviate_repository.chunk_exists(uuid_str, class_name):
                    logger.info(
                        f"[SKIP][W{batch_id}] Chunk {i + 1}/{len(chunks)} already exists - arxiv_id: {arxiv_id}")
                    continue

                try:
                    weaviate_repository.create(arxiv_id, chunk, class_name, vector, uuid_str)
                    logger.info(f"[SAVE][W{batch_id}] Chunk {i + 1}/{len(chunks)} saved successfully")
                except Exception as e:
                    logger.error(
                        f"[ERROR][W{batch_id}] Failed to save chunk - arxiv_id: {arxiv_id}, Chunk {i + 1}: {e}")

            logger.info(f"[DONE][W{batch_id}] Finished processing - arxiv_id: {arxiv_id}")

        except Exception as e:
            logger.error(f"[ERROR][W{batch_id}] Unexpected error during processing - {e}")
