from argparse import ArgumentParser


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--model", dest="model_name", type=str, default="all-MiniLM-L6-v2",
                        help="SentenceTransformer model name")
    parser.add_argument("--class-name", dest="class_name", type=str, default="ArxivChunkMiniLML6v2",
                        help="Weaviate class name")
    parser.add_argument("--device", dest="device", type=str, default="cpu", help="device")
    parser.add_argument("--logs", dest="log_name", type=str, default="app-default", help="log file name")
    return parser.parse_args()
