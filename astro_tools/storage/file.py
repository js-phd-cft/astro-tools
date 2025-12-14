from pathlib import Path

class FileBackend:
    def __init__(self, base_path=None):
        self.base = Path(base_path or '/data')
    
    def save_fits(self, hdu_list, path):
        dest = self.base / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        hdu_list.writeto(dest, overwrite=True)
        return str(dest)