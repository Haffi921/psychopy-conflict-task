fixation_cross = dict(
    start = 0.0,
    stop = 1.0,
    type = "ShapeStim",
    spec = dict(
        name = "fixation_cross",
        vertices = "cross",
        size = 0.05,
        lineColor = None,
        fillColor = "white",
    )
)

distractor = dict(
    start = 1.0,
    stop = 1.133,
    type = "TextStim",
    spec = dict(
        name = "distractor",
        color = "white",
        height = 0.05,
    ),
    variable = dict(
        text = "distractor_text"
    )
)

target = dict(
    start = 1.166,
    stop = 1.3,
    type = "TextStim",
    spec = dict(
        name = "target",
        color = "white",
        height = 0.05,
    ),
    variable = dict(
        text = "target_text",
    )
)

response = dict(
    start = 1.3,
    stop = 3.0,
    keys = ["a", "d", "j", "l"],
    variable = dict(
        correct_resp = "correct_resp",
    )
)