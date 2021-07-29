from psychopy import clock

from .component import *

class Trial:
    response: ResponseComponent
    visual: list[VisualComponent]
    audio: list[AudioComponent]
    wait: list[WaitComponent]

    clock = clock.Clock()

    def __init__(self, window, componentSettings):
        if "response" in componentSettings:
            self.response = ResponseComponent(componentSettings["response"])
        
        if "visual_components" in componentSettings:
            for component in componentSettings["visual_components"]:
                self.visual.append(VisualComponent(window, component))
        
        if "audio_components" in componentSettings:
            for component in componentSettings["audio_components"]:
                self.audio.append(AudioComponent(window, component))
        
        if "wait_components" in componentSettings:
            for component in componentSettings["wait_components"]:
                self.wait.append(WaitComponent(component))

    def _get_all_components(self) -> list[BaseComponent]:
        return [
            self.response,
            *self.visual,
            *self.audio,
            *self.wait,
        ]
    
    def _refresh(self):
        for component in self._get_all_components():
            component.refresh()