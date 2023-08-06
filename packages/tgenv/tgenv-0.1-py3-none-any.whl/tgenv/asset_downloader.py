import math
import requests

from tqdm import tqdm # type: ignore


def download_asset(url: str, out_file: str, github_token: str):
    """ Starts a download stream and displays a loading bar.

    :param url: The url to download from
    :type url: str
    :param out_file: The file to write
    :type out_file: str
    :param github_token: [description]
    :type github_token: str
    :raises DownloadException: [description]
    """
    if github_token:
        header = {"Authorization": "token" + github_token}
    else:
        header = {}
    download_stream = requests.get(url, stream=True, headers=header)

    size = int(download_stream.headers.get('content-length', 0))
    block_size = 1024
    written = 0
    total = math.ceil(size//block_size)
    stream_iterable = download_stream.iter_content(block_size)
    with open(out_file, 'wb') as asset:
        for data in tqdm(stream_iterable, total=total , unit='KB', unit_scale=1):
            written = written  + len(data)
            asset.write(data)
    if size not in (0, written):
        raise DownloadException("Error while downloading file.")

class DownloadException(Exception):
    """ A generic downloader exception
    """
    def __init__(self, *args):
        Exception.__init__(self, args)
