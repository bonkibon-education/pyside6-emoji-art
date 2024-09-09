from util import UtilMetaSingleton


class DefaultController(metaclass=UtilMetaSingleton):
    _controllers: dict = dict()

    def register_controller(self, name: str):
        self._controllers[name] = self

    def get_controller(self, name):
        return self._controllers[name]
