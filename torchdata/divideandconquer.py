CHUNK_SIZE = (1024**2) * 50
file_number = 1
with open('encoder-5-3000.pkl', 'rb') as f:
    chunk = f.read(CHUNK_SIZE)
    while chunk:
        with open('encoder-5-3000_part_' + str(file_number), 'wb') as chunk_file:
            chunk_file.write(chunk)
        file_number += 1
        chunk = f.read(CHUNK_SIZE)
