from langchain.text_splitter import RecursiveCharacterTextSplitter


def split_text(text, chunk_size=512, overlap=64):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", ".", " "]
    )
    return splitter.split_text(text)
