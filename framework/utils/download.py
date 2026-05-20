import shutil
import time
from pathlib import Path

from framework.core.logger import get_logger

logger = get_logger(__name__)


class DownloadUtils:
    DOWNLOADS_DIR_NAME = "downloads"
    CHROME_TEMP_EXTENSION = ".crdownload"
    FIREFOX_TEMP_EXTENSION = ".part"

    @staticmethod
    def directory() -> Path:
        download_dir = Path(__file__).resolve().parents[2] / DownloadUtils.DOWNLOADS_DIR_NAME
        download_dir.mkdir(parents=True, exist_ok=True)
        return download_dir

    @staticmethod
    def prepare_directory() -> Path:
        download_dir = DownloadUtils.directory()
        logger.info("Preparing download directory: path='%s'", download_dir)
        if download_dir.exists():
            shutil.rmtree(download_dir)
        download_dir.mkdir(parents=True)
        return download_dir

    @staticmethod
    def wait_for_file(file_path: Path, timeout: int = 10) -> Path:
        logger.info("Waiting for downloaded file: path='%s', timeout=%s", file_path, timeout)
        deadline = time.monotonic() + timeout
        temporary_file_paths = [
            Path(f"{file_path}{DownloadUtils.CHROME_TEMP_EXTENSION}"),
            Path(f"{file_path}{DownloadUtils.FIREFOX_TEMP_EXTENSION}"),
        ]

        while time.monotonic() < deadline:
            if (
                file_path.exists()
                and file_path.stat().st_size > 0
                and not any(path.exists() for path in temporary_file_paths)
            ):
                logger.info("Downloaded file is ready: path='%s', size=%s", file_path, file_path.stat().st_size)
                return file_path
            time.sleep(0.1)

        raise AssertionError(f"Downloaded file was not found: {file_path}")
