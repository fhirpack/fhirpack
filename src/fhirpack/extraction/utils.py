def chunker(seq, size):
    for pos in range(0, len(seq), size):
        yield seq[pos : pos + size]
