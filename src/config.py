import yaml

class Config:
    """_summary_
    """
    def __init__(self):
        with open("./../settings/config.yaml", 'r',encoding="UTF-8") as file:
            self.config = yaml.safe_load(file)
