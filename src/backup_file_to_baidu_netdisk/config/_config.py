

class Config:
    ...

_config = None

def get_config():
    global _config
    if _config is None:
        _config = Config()
    return _config