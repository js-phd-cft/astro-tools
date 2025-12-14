from pathlib import Path

class FileBackend:
    def __init__(self, base_path=None):
        """
        File storage backend.
        
        Args:
            base_path: Base directory for storage (defaults to STORAGE_PATH env var or '/data')
        """
        default_path = os.getenv('STORAGE_PATH', '/data')
        self.base = Path(base_path or default_path)
    
    def save_fits(self, hdu_list, path):
        dest = self.base / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        hdu_list.writeto(dest, overwrite=True)
        return str(dest)