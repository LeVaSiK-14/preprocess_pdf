

def get_tile_starts(dim_size, tile_size, overlap):
    starts = []
    step = tile_size - overlap
    pos = 0
    while True:
        if pos > dim_size - tile_size:
            break
        starts.append(pos)
        pos += step
    last_pos = dim_size - tile_size
    if last_pos not in starts:
        if starts and starts[-1] < last_pos:
            starts.append(last_pos)
        elif not starts:
            starts.append(0)
    return starts
