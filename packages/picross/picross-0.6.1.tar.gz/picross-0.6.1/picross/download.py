from . import conf
from pathlib import Path
import subprocess


class DownloadConfigIncompleteError(Exception):
    pass


class DownloadConfigNotFoundError(Exception):
    pass


def download(url):
    # url: GeminiUrl
    try:
        if not conf.get("download-cmd") or not conf.get("download-dest"):
            raise DownloadConfigIncompleteError
        download_dest = Path(conf.get("download-dest")).expanduser()
        download_cmd = (
            conf.get("download-cmd")
            .replace("$URL", str(url))
            .replace("$DEST", str(download_dest))
        )
    except KeyError:
        raise DownloadConfigNotFoundError

    proc = subprocess.run(download_cmd, shell=True)

