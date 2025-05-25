from argparse import ArgumentParser


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--model", dest="model_name", type=str, default="all-MiniLM-L6-v2",
                        help="SentenceTransformer model name")
    parser.add_argument("--class", dest="class_name", type=str, default="ArxivChunkMiniLML6v2",
                        help="Weaviate class name")
    parser.add_argument("--device", dest="device", type=str, default="cpu", help="device")
    return parser.parse_args()
