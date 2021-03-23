from datetime import datetime
from pathlib import Path


def get_basic_dirpath(timestamp=None):
    if not timestamp:
        timestamp = str(datetime.now().strftime('%Y%m%d_%H%M%S'))
    basic_dirpath = Path(
        Path.home(),
        'Downloads',
        'wordpress-parse',
        timestamp
    )
    # if dirpath and dirpath.exists():
    #     shutil.rmtree(dirpath)
    #     dirpath.mkdir()
    if basic_dirpath:
        basic_dirpath.mkdir(parents=True, exist_ok=True)
    return basic_dirpath
