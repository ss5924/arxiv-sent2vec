import asyncio

import logging_config
import models
import sent2vec_processor
import utils
import weaviate_repository
from config import MAX_CONCURRENT_TASKS, BATCH_SIZE
from database import mongo_collection
from logging_config import logger

logging_config.setup_logger()


async def main():
    args = utils.parse_args()

    logger.info(f"model-name:{args.model_name}, device:{args.device}, class-name{args.class_name}")

    model = models.load_model(args.model_name, args.device)

    weaviate_repository.create_weaviate_schema(args.class_name)

    semaphore = asyncio.Semaphore(MAX_CONCURRENT_TASKS)

    total_docs = await mongo_collection.count_documents({})

    for skip in range(0, total_docs, BATCH_SIZE):
        cursor = mongo_collection.find().skip(skip).limit(BATCH_SIZE)
        docs = await cursor.to_list(length=BATCH_SIZE)

        tasks = [
            sent2vec_processor.process_paper(doc, semaphore, args.class_name, batch_id=i, model=model)
            for i, doc in enumerate(docs)
        ]
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
