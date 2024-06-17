import contextvars
from srint.core.models import Config
class ContextManager():
    app_config: Config = contextvars.ContextVar("app_config", default=None)

    @classmethod
    def set_config(cls, config:Config):
        cls.app_config.set(config)

    @classmethod
    def get_config(self)->Config:
        return self.app_config.get()