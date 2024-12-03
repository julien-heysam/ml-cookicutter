import os.path
import signal
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from threading import Event
from typing import Optional, List
from urllib.request import Request, urlopen

from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TaskID,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)

class DownloadUtils:
    def __init__(self, max_workers: int = 4):
        """Initialize the download manager.
        
        Args:
            max_workers: Maximum number of concurrent downloads
        """
        self.progress = Progress(
            TextColumn("[bold blue]{task.fields[filename]}", justify="right"),
            BarColumn(bar_width=None),
            "[progress.percentage]{task.percentage:>3.1f}%",
            "•",
            DownloadColumn(),
            "•",
            TransferSpeedColumn(),
            "•",
            TimeRemainingColumn(),
        )
        self.done_event = Event()
        self.max_workers = max_workers
        
        # Setup signal handler
        signal.signal(signal.SIGINT, self._handle_sigint)

    def _handle_sigint(self, signum, frame):
        """Handle SIGINT (Ctrl+C) signal."""
        self.done_event.set()

    def _copy_url(self, url: str, path: str, task_id: Optional[TaskID] = None) -> None:
        """Download a single file from URL to the specified path."""
        try:
            self.progress.console.log(f"Requesting {url}")
            request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
            response = urlopen(request)
            total_size = int(response.info()["Content-Length"])
            
            if task_id is not None:
                self.progress.update(task_id, total=total_size)
                
            with open(path, "wb") as dest_file:
                if task_id is not None:
                    self.progress.start_task(task_id)
                    
                for data in iter(partial(response.read, 32768), b""):
                    dest_file.write(data)
                    if task_id is not None:
                        self.progress.update(task_id, advance=len(data))
                    if self.done_event.is_set():
                        return
                        
            self.progress.console.log(f"Downloaded {path}")
            
        except Exception as e:
            self.progress.console.log(f"Failed to download {url}: {e}")

    def download_urls(self, urls: List[str], dest_dir: str) -> None:
        """Download multiple files to the given directory.
        
        Args:
            urls: List of URLs to download
            dest_dir: Destination directory for downloaded files
        """
        with self.progress:
            with ThreadPoolExecutor(max_workers=self.max_workers) as pool:
                for url in urls:
                    filename = url.split("/")[-1]
                    dest_path = os.path.join(dest_dir, filename)
                    task_id = self.progress.add_task("download", filename=filename, start=False)
                    self.progress.console.log(f"Starting download for {url}")
                    pool.submit(self._copy_url, url, dest_path, task_id)
