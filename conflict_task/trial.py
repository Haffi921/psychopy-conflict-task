from psychopy import clock
from .component import VisualComponent, ResponseComponent, BaseComponent
from .util import Alternator, Randomizer

class Trial:
    # TODO: Add AudioComponents, etc.
    visualComponents = []
    
    # Main conflict-task components
    distractor = None
    target = None
    response = None

    randomizer = None
    alternator = None

    clock = clock.Clock()

    def __init__(self, window, visualComponents, response):
        for component in visualComponents:
            visualComponent = VisualComponent(window, component)

            if visualComponent.visual.name == "distractor":
                self.distractor = visualComponent
            if visualComponent.visual.name == "target":
                self.target = visualComponent
            
            self.visualComponents.append(visualComponent)

        self.randomizer = Randomizer(self.target.variable_factor["random_max"])
        if self.target.alternating:
            self.alternator = Alternator(self.target.variable_factor["alternator"])
        
        self.response = ResponseComponent(response)
        
        if self.any_alternating:

            self.alternator = Alternator()

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