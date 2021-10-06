fixation_cross = dict(
    start=0.0,
    stop=0.75,
    type="ShapeStim",
    spec=dict(
        name="fixation_cross",
        vertices="cross",
        size=0.05,
        lineColor=None,
        fillColor="white",
    ),
)

distractor = dict(
    start=0.75,
    stop=1.7,
    type="TextStim",
    spec=dict(
        name="distractor",
        color="white",
        height=0.1,
        font="Lucida Sans Typewriter",
    ),
    variable=dict(text="distractor_text"),
)

target = dict(
    start=0.85,
    stop=1.7,
    type="TextStim",
    spec=dict(
        name="target",
        color="white",
        height=0.1,
        font="Lucida Sans Typewriter",
    ),
    variable=dict(
        text="target_text",
    ),
)

response = dict(
    start=0.85,
    stop=2.0,
    keys=["left", "right"],
    variable=dict(
        correct_key="correct_key",
    ),
)
