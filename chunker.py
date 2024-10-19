from langchain.text_splitter import CharacterTextSplitter

def chunk_text(raw_text):
    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=200, length_function=len)
    chunk = text_splitter.split_text(raw_text)
    return chunk