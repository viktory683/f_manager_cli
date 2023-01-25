def split_by_len(text: str, chunk_size: int):
    """Splits text into chunks

    Args:
        text (str): Text to split
        chunk_size (int): Length of chunks to split

    Returns:
        list[str]: List of chunks
    """
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
