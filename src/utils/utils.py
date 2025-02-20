from pathlib import Path
import sys
import os

from dotenv import load_dotenv


ENV_PATH = Path(f'{os.getcwd()}/.env')
load_dotenv(dotenv_path=ENV_PATH, override=True)


def get_env(env_name: str) -> str:
    return os.getenv(env_name)


def get_nested_value(d, *keys):
    for key in keys:
        if isinstance(d, list):
            if not isinstance(key, int) or key >= len(d):
                return None
            d = d[key]
        elif isinstance(d, dict):
            d = d.get(key)
        else:
            return None
    return d


def set_current_directory() -> str:
    """Get current directory of current .py execution

    Returns:
        str: The path
    """

    directory: str = ''
    
    # determine if application is a script file or frozen exe
    if getattr(sys, 'frozen', False):
        # Running as a PyInstaller bundle
        application_path = os.path.dirname(sys.executable)
        directory = os.path.abspath(os.path.join(application_path))
    elif __file__:
        # Running as a standard Python script
        application_path = os.path.dirname(__file__)
        directory = os.path.abspath(os.path.join(application_path, '..'))

    # set current directory
    os.chdir(directory)

    return directory
