"""Module that stores the Config object.

Raises
------
RuntimeError
    When called as the main script and not imported
"""
import yaml
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
            with open("./../settings/config.yaml", 'r',encoding="UTF-8") as file:
                self.config = yaml.safe_load(file)
        except:
            raise FileNotFoundError("Failed to load or parse the config file.")
    
if __name__ == "__main__":
    raise RuntimeError("This module is designed for import only.")