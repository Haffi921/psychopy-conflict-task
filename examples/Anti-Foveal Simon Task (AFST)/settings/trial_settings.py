fixation_cross = dict(
    start=0.0,
    stop=0.5,
    type="ShapeStim",
    spec=dict(
        name="fixation_cross",
        vertices="cross",
        size=0.025,
        lineColor=None,
        fillColor="white",
    ),
)

circle = dict(
    start=0.0,
    stop=3.5,
    type="Circle",
    spec=dict(name="circle", edges=128, radius=0.05, lineColor="black", fillColor=None),
)

target = dict(
    start=1.0,
    stop=3.5,
    type="TextStim",
    spec=dict(
        name="target",
        color="white",
        height=0.02,
    ),
    variable=dict(
        text="target_text",
        pos="target_pos",
    ),
)

response = dict(
    start=1.0,
    stop=3.5,
    keys=["left", "right", "up", "down"],
    variable=dict(
        correct_key="correct_key",
    ),
)
