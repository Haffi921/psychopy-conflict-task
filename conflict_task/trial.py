from psychopy import clock
from .component import VisualComponent, ResponseComponent, BaseComponent

componentList = list[BaseComponent]

class Trial:
    visualComponents = []
    response = None
    any_alternating = False
    any_random = False

    clock = clock.Clock()

    def __init__(self, window, visualComponents, response):
        for component in visualComponents:
            self.visualComponents.append(VisualComponent(window, component))
            if self.visualComponents[-1].random:
                self.any_random = True
            if self.visualComponents[-1].alternating:
                self.any_alternating = True
        
        self.response = ResponseComponent(response)
        if self.response.alternating:
            self.any_alternating = True

    def get_all_components(self) -> list[BaseComponent]:
        return [*self.visualComponents, self.response]

    def refresh(self):
        for component in self.get_all_components():
            component.refresh()
    
    def run(self, window, input_device, frameTolerance):
        self.refresh()
        running = True
        time = 0
        self.clock.reset(-window.getFutureFlipTime(clock="now"))

        while running:
            if input_device.getKeys(["escape"]):
                return False
            
            t = self.clock.getTime()
            thisFlip = window.getFutureFlipTime(clock=self.clock)
            thisFlipGlobal = window.getFutureFlipTime(clock=None)

            running = False

            for component in self.get_all_components():
                if component.not_started():
                    if thisFlip >= component.start_time - frameTolerance:
                        component.start(time, thisFlipGlobal)
                elif component.started():
                    if thisFlip >= component.stop_time - frameTolerance:
                        component.stop(time, thisFlipGlobal)
                
                if not component.finished():
                    running = True
            
            self.response.check(input_device)

            window.flip()
        
        return True