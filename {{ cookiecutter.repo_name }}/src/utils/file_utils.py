import json
import logging
import os
from pathlib import Path
from typing import Union, List, Dict, Optional

logger = logging.getLogger(__name__)


class FileUtils:
    """A utility class for file operations including reading, writing, and directory management."""

    @staticmethod
    def write_text(text: str, path: Union[str, Path]) -> None:
        """
        Write text content to a file.
        
        Args:
            text: The text content to write
            path: The target file path
        """
        with open(path, "w") as file:
            file.write(text)
        logger.info(f"Created file: {path}")

    @staticmethod
    def read_text(path: Union[str, Path], as_list: bool = False) -> Union[List[str], str]:
        """
        Read content from a text file.
        
        Args:
            path: The file path to read from
            as_list: If True, returns content as list of lines; if False, returns as single string
            
        Returns:
            Either a list of strings (lines) or a single string based on as_list parameter
            
        Raises:
            FileNotFoundError: If the specified file doesn't exist
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"File {path} does not exist")
            
        with open(path, "r") as file:
            lines = file.readlines()

        if as_list:
            return [line.strip() for line in lines]
        return "".join(lines).strip()

    @staticmethod
    def read_json(path: Union[str, Path]) -> Dict:
        """
        Read and parse a JSON file.
        
        Args:
            path: Path to the JSON file
            
        Returns:
            Dict containing the parsed JSON data
            
        Raises:
            FileNotFoundError: If the specified file doesn't exist
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"File {path} does not exist")
            
        with open(path, "r") as f:
            return json.load(f)

    @staticmethod
    def write_json(data: Dict, path: Union[str, Path], indent: int = 4) -> None:
        """
        Write data to a JSON file.
        
        Args:
            data: Dictionary to be written as JSON
            path: Target file path
            indent: Number of spaces for indentation in the JSON file
        """
        with open(path, "w") as f:
            json.dump(data, f, indent=indent)
        logger.info(f"Written JSON to file: {path}")

    @staticmethod
    def ensure_directory(file_path: Union[str, Path]) -> None:
        """
        Ensure the directory exists for a given file path, creating it if necessary.
        
        Args:
            file_path: Path to file or directory to ensure exists
        """
        path = Path(file_path) if isinstance(file_path, str) else file_path
        directory = path.parent
        directory.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Ensured directory exists: {directory}")

    @staticmethod
    def list_directories(
        path: Union[str, Path], 
        exclude_patterns: Optional[List[str]] = None
    ) -> List[str]:
        """
        Recursively list all directories under the specified path.
        
        Args:
            path: Root path to start the directory search
            exclude_patterns: List of patterns to exclude from the search
            
        Returns:
            List of directory paths
        """
        exclude_patterns = set(exclude_patterns or [])

        def should_exclude(dir_path: str) -> bool:
            return any(pattern in dir_path for pattern in exclude_patterns)

        directories = []
        for root, dirs, _ in os.walk(str(path)):
            dirs[:] = [d for d in dirs if not should_exclude(os.path.join(root, d))]
            directories.extend(os.path.join(root, d) for d in dirs)
            
        return directories
