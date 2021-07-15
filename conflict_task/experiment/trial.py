from psychopy import clock
from .component import VisualComponent, ResponseComponent, BaseComponent

class Trial:
    # TODO: Add AudioComponents, etc.
    visualComponents = []
    
    # Main conflict-task components
    response = None

    clock = clock.Clock()

    def __init__(self, window, visualComponents, response):
        for component in visualComponents:
            visualComponent = VisualComponent(window, component)
            
            self.visualComponents.append(visualComponent)
                
        self.response = ResponseComponent(response)

    def get_all_components(self) -> list[BaseComponent]:
        return [*self.visualComponents, self.response]

    def refresh(self):
        for component in self.get_all_components():
            component.refresh()
    
    def run(self, trial_values, experiment):
        self.refresh()

        for component in self.get_all_components():
            component.prepare(trial_values)

        running = True
        self.clock.reset(-experiment.window.getFutureFlipTime(clock="now"))
        
        while running:
            if experiment.input_device.getKeys(["escape"]):
                return False
            
            time = self.clock.getTime()
            thisFlip = experiment.window.getFutureFlipTime(clock=self.clock)
            thisFlipGlobal = experiment.window.getFutureFlipTime(clock=None)

            running = False

            for component in self.get_all_components():
                if component.not_started():
                    if thisFlip >= component.start_time - experiment.frameTolerance:
                        component.start(time, thisFlipGlobal)
                elif component.started():
                    if thisFlip >= component.stop_time - experiment.frameTolerance:
                        component.stop(time, thisFlipGlobal)
                
                if not component.finished():
                    running = True
            
            self.response.check(experiment.input_device)

            experiment.window.flip()
        
        return True