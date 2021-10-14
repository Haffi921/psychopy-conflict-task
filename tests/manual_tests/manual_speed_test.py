from time import perf_counter

from conflict_task.devices import Keyboard, Window
from conflict_task.sequence import Trial

win = Window({"fullscr": False, "size": (1, 1)})
input = Keyboard()

visual_components = []

forloop_tic = perf_counter()
for i in range(1, 100):
    visual_components.append(
        {
            "name": "Text" + str(i),
            "type": "TextStim",
            "stop": 1.0,
            "spec": {},
        }
    )
forloop_toc = perf_counter()
print(f"For loop: {forloop_toc - forloop_tic}")

trial_creation_tic = perf_counter()
trial = Trial(
    win,
    input,
    {
        "name": "TestScreen",
        "visual_components": visual_components,
        "response": {"keys": ["space"], "stop": 1.0},
    },
)
trial_creation_toc = perf_counter()
print(f"Trial creation: {trial_creation_toc - trial_creation_tic}")

get_data_tic = perf_counter()
data1 = trial.get_data()
get_data_toc = perf_counter()
print(f"get_data1: {get_data_toc - get_data_tic}")

# get_data2_tic = perf_counter()
# data2 = trial.get_data2()
# get_data2_toc = perf_counter()
# print(f"get_data2: {get_data2_toc - get_data2_tic}")
