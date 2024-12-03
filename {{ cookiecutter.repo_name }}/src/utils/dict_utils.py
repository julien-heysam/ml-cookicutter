import json
from typing import Any, Dict, List, TypeVar, Union, Optional

from src.utils.text_utils import TextUtils

T = TypeVar('T')

class DictionaryUtils:
    """A utility class for dictionary and nested data structure operations."""
    
    @staticmethod
    def flatten_list(nested_list: List[Any]) -> List[Any]:
        """
        Flattens a nested list into a single-level list.
        
        Args:
            nested_list: A potentially nested list structure
            
        Returns:
            A flattened list containing all elements
        """
        return list(DictionaryUtils._flatten_list_generator(nested_list))
    
    @staticmethod
    def _flatten_list_generator(nested_list: List[Any]):
        """Internal generator method for list flattening."""
        for item in nested_list:
            if isinstance(item, list):
                yield from DictionaryUtils._flatten_list_generator(item)
            else:
                yield item

    @staticmethod
    def sanitize_json(data: Union[str, Dict, List, Any]) -> Optional[Any]:
        """
        Sanitizes JSON data by cleaning strings and handling nested structures.
        
        Args:
            data: Input data that can be a JSON string, dict, list, or other types
            
        Returns:
            Sanitized data structure or None if invalid JSON string
        """
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                return None

        if isinstance(data, dict):
            return {k: DictionaryUtils.sanitize_json(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [DictionaryUtils.sanitize_json(item) for item in data]
        elif isinstance(data, str):
            return TextUtils.sanitize_string(data)
        return data

    @staticmethod
    def flatten_dict(
        d: Dict[str, Any],
        parent_key: str = "",
        sep: str = "_"
    ) -> Dict[str, Any]:
        """
        Flattens a nested dictionary into a single-level dictionary.
        
        Args:
            d: The input dictionary to flatten
            parent_key: Key prefix for nested dictionary items
            sep: Separator to use between nested keys
            
        Returns:
            A flattened dictionary with concatenated keys
        """
        items: List[tuple] = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(
                    DictionaryUtils.flatten_dict(v, new_key, sep=sep).items()
                )
            else:
                items.append((new_key, v))
        return dict(items)

    @staticmethod
    def replace_values(
        d: Dict[str, T],
        value_to_replace: Any = None,
        default_value: T = "",
        recursive: bool = False
    ) -> Dict[str, T]:
        """
        Replaces specified values in a dictionary with a default value.
        
        Args:
            d: Input dictionary
            value_to_replace: Value to be replaced
            default_value: Value to use as replacement
            recursive: Whether to process nested dictionaries
            
        Returns:
            Dictionary with replaced values
        """
        if not recursive:
            return {
                k: default_value if v == value_to_replace else v 
                for k, v in d.items()
            }
        
        result = {}
        for k, v in d.items():
            if isinstance(v, dict):
                result[k] = DictionaryUtils.replace_values(
                    v, value_to_replace, default_value, recursive=True
                )
            else:
                result[k] = default_value if v == value_to_replace else v
        return result
