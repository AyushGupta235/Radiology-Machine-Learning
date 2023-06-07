import os
from box.exceptions import BoxValueError
import yaml
from TransUNet import logger
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any
import base64

@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """Read yaml file and return a ConfigBox object.
    
    Args:
        path_to_yaml: Path to yaml file.
    
    Raises:
        BoxValueError: If the yaml file is empty.

    Returns:
        ConfigBox: ConfigBox object.
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"Loaded yaml file from {path_to_yaml}")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError(f"Yaml file {path_to_yaml} is empty.")
    except Exception as e:
        raise e
    

@ensure_annotations
def create_directories(path_to_dir: list, verbose=True) -> None:
    """Create directories if they do not exist.
    
    Args:
        path_to_dir: Path to directory.
        ignore_log (bool, optional): ignore if multiple dirs is to be created. Defaults to False.
    """
    for path in path_to_dir:
        if not os.path.exists(path):
            os.makedirs(path)
            if verbose:
                logger.info(f"Created directory {path}")
        else:
            if verbose:
                logger.info(f"Directory {path} already exists.")


@ensure_annotations
def save_json(path_to_json: Path, data: Any) -> None:
    """Save json file.
    
    Args:
        path_to_json: Path to json file.
        data: Data to be saved.
    """
    with open(path_to_json, "w") as f:
        json.dump(data, f)
        logger.info(f"Saved json file to {path_to_json}")


@ensure_annotations
def load_json(path_to_json: Path) -> ConfigBox:
    """Load json file data.
    
    Args:
        path_to_json: Path to json file.
    
    Returns:
        Any: Loaded json file.
    """
    with open(path_to_json, "r") as f:
        content = json.load(f)
        logger.info(f"Loaded json file from {path_to_json}")
    
    return ConfigBox(content)


@ensure_annotations
def save_bin(data: Any, path: Path) -> None:
    """Save binary file.
    
    Args:
        data: Data to be saved.
        path: Path to file.
    """
    joblib.dump(value=data, filename=path)
    logger.info(f"Binary file saved at {path}")


@ensure_annotations
def load_bin(path: Path) -> Any:
    """Load binary file.
    
    Args:
        path: Path to file.
    
    Returns:
        Any: Loaded binary file.
    """
    data = joblib.load(path)
    logger.info(f"Loaded binary file from {path}")
    return data


@ensure_annotations
def get_size(path: Path) -> str:
    """Get size of file in KB.
    
    Args:
        path: Path to file.
    
    Returns:
        str: Size of file.
    """
    size = round(os.path.getsize(path) / 1024)
    return f"{size} KB"


@ensure_annotations
def decodeImage(imgstring, filename):
    """Decode image from base64 string.
    
    Args:
        imgstring: Base64 string.
        filename: Name of file.
    
    Returns:
        str: Path to file.
    """
    imgdata = base64.b64decode(imgstring)
    with open(filename, "wb") as f:
        f.write(imgdata)
        f.close()

    logger.info(f"Image saved at {filename}")


def encodeImage(ImagePath):
    """Encode image to base64 string.
    
    Args:
        ImagePath: Path to image.
    
    Returns:
        str: Base64 string.
    """
    with open(ImagePath, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")