from typing import Callable
import functools
import hashlib
import json
import os


def persistent_cache(
    directory: str, hash_filenames: bool = False, file_type="json"
) -> Callable:
    """
    A decorator to cache function outputs to individual files in the specified directory.
    Each function call result is stored in a separate file. Filenames can be hashed or kept as the argument value.

    Args:
        directory (str): Path to the directory where cache files will be stored.
        hash_filenames (bool): Whether to hash filenames. Default is False.

    Returns:
        Callable: The decorated function.
    """

    def decorator(func: Callable) -> Callable:
        os.makedirs(directory, exist_ok=True)

        @functools.wraps(func)
        def wrapper(arg):
            if hash_filenames:
                filename = hashlib.sha256(str(arg).encode()).hexdigest()
            else:
                if "/" in arg:
                    filename = arg.replace("/", "_")
                else:
                    filename = str(arg)
            cache_file = os.path.join(directory, f"{filename}.{file_type}")

            if os.path.exists(cache_file):
                with open(cache_file, "r") as f:
                    if file_type == "json":
                        return json.load(f)
                    else:
                        file_contents = f.read()
                        return file_contents

            result = func(arg)
            with open(cache_file, "w") as f:
                if file_type == "json":
                    json.dump(result, f)
                else:
                    f.write(result)

            return result

        return wrapper

    return decorator
