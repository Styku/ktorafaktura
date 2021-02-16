import yaml

class Config:
    _config = {}

    @classmethod
    def load(cls, path = 'config.yaml'):
        print('Loading config from {}'.format(path))
        with open(path, 'r') as f:
            cls._config = yaml.load(f, Loader=yaml.FullLoader)

    @classmethod
    def save(cls, path = 'config.yaml'):
        with open(path, 'r') as f:
            cls._config = yaml.load(f, Loader=yaml.FullLoader)

    @classmethod
    def get(cls, property):
        return cls._config[property]

    @classmethod
    def set(cls, property, value):
        cls._config[property] = value

