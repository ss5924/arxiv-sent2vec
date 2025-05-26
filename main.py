import asyncio
import logging

import logging_config
import models
import sent2vec_processor
import utils
import weaviate_repository
from config import MAX_CONCURRENT_TASKS, BATCH_SIZE
from database import mongo_collection


async def main():
    args = utils.parse_args()

    logging_config.setup_logger(log_name=args.log_name)
    logger = logging.getLogger(__name__)

    logger.info(
        "Model name: %s\nDevice: %s\nClass name: %s\nLogs file name: %s",
        args.model_name, args.device, args.class_name, args.log_name
    )

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
