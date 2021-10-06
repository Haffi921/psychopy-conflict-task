from ._base_component import BaseComponent


class WaitComponent(BaseComponent):
    def __init__(self, component_settings, window=None):
        super().__init__(component_settings)
