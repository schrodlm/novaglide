"""Module that stores the Config object.

Raises
------
RuntimeError
    When called as the main script and not imported
"""
import yaml
from typing import Any
class Config:
    """
    Config class for managing configuration settings.

    Attributes
    ----------
    config : dict
        A dictionary containing the configuration settings.

    Raises
    ------
    FileNotFoundError
        If the config file is not found or there is an issue parsing it.
    """
    def __init__(self):
        try:
            with (open("./../settings/config.yaml", 'r',encoding="UTF-8")
                as file):
                self.config = yaml.safe_load(file)
        except:
            raise FileNotFoundError("Failed to load or parse the config file.")
       
    def __getitem__(self,key: str) -> Any:
        """
        Returns the value associated with the specified key 
        from the configuration settings.

        Parameters
        ----------
        key : str
            The key for retrieving a specific configuration setting.

        Returns
        -------
        Any
            The value associated with the specified key.

        Notes
        -----
        This method allows accessing configuration settings using square bracket notation (e.g., config['key']).
        """
        #ensuring by name indexing
        return self.config[key]
    
if __name__ == "__main__":
    raise RuntimeError("This module is designed for import only.")