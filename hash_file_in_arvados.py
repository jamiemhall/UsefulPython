import arvados
import arvados.collection
import hashlib
import os

BLOCK_SIZE = 65_536
API_CONFIG = {
    'ARVADOS_API_TOKEN': os.environ.get('ARVADOS_API_TOKEN'),
    'ARVADOS_API_HOST': os.environ.get('ARVADOS_API_HOST'),
    'ARVADOS_API_HOST_INSECURE': os.environ.get('ARVADOS_API_HOST_INSECURE')
}


def hash_arvados_filestream(filestream: arvados.arvfile.ArvadosFileReader) -> str:
    md5 = hashlib.md5()
    for data in iter(lambda: filestream.read(BLOCK_SIZE), b''):
        md5.update(data)

    return md5.hexdigest()


def retrieve_arv_file_stream(collection: arvados.collection.CollectionReader, filename: str):
    try:
        fh = collection.open(filename, "rb")
    except (IOError, EOFError) as e:
        return None
    except Exception:
        return None
    else:
        return fh


def search_collection_for_file(collection: arvados.collection.CollectionReader, filename: str) -> arvados.arvfile.ArvadosFileReader:
    filestream = retrieve_arv_file_stream(collection, filename)
    if filestream:
        return filestream
    else:
        for item in collection.values():
            if isinstance(item, arvados.collection.Subcollection):
                result = search_collection_for_file(item, filename)
                if result:
                    return retrieve_arv_file_stream(item, filename)


def main(uuid: str, filename: str) -> str:
    collection_reader = arvados.collection.CollectionReader(uuid, apiconfig=API_CONFIG)
    filestream = search_collection_for_file(collection=collection_reader, filename=filename)
    if not filestream:
        return f'{filename} not found in collection {uuid}'

    md5_hash = hash_arvados_filestream(filestream)
    return md5_hash
