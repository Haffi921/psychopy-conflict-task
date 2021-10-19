font_family = "Courier New"

fixation_cross = {
    "stop": 0.2,
    "type": "ShapeStim",
    "spec": {
        "name": "fixation_cross",
        "vertices": "cross",
        "size": 64,
        "lineColor": None,
        "fillColor": "black",
    },
    "variable": {"opacity": "fixation_opacity"},
}

distractor = {
    "start": 1.0,
    "stop": 1.133,
    "type": "TextStim",
    "spec": {
        "name": "distractor",
        "color": "black",
        "height": 64,
        "font": font_family,
    },
    "variable": {
        "text": "distractor_text",
    },
}

target = {
    "start": 1.166,
    "stop": 1.3,
    "type": "TextStim",
    "spec": {"name": "target", "color": "black", "height": 103, "font": font_family},
    "variable": {
        "text": "target_text",
    },
}

response = {
    "start": 1.3,
    "duration": 1.383,
    "keys": ["f", "g", "j", "n"],
    "variable": {
        "correct_key": "correct_key",
    },
}

feedback = {
    "stop": 0.2,
    "type": "TextStim",
    "spec": {"name": "feedback", "color": "black", "height": 80, "font": font_family},
    "variable": {
        "text": "feedback_text",
        "opacity": "feedback_opacity",
    },
}

trial = {
    "type": "Trial",
    "visual_components": [distractor, target],
    "response": response,
    "takes_trial_values": True,
    "feedback": True,
    "feedback_sequence": {
        "visual_components": [feedback, fixation_cross],
        "trial_values": lambda trial: {
            **trial,
            "feedback_text": "Zu langsam"
            if not trial["response_made"]
            else ("Fehler" if not trial["response_correct"] else ""),
            "fixation_opacity": 1.0 if trial["response_correct"] else 0.0,
        },
    },
}

# if __name__ == "__main__":
#     from conflict_task.preview import preview_sequence, preview_component

#     # preview_component(fixation_cross, {
#     #         "distractor_text": "Left\nLeft\nLeft",
#     #         "target_text": "Right",
#     #         "correct_key": "f",
#     #         "feedback_text": "Fehler"
#     #     }, {"units": "pix"})

#     # preview_sequence(
#     #     trial,
#     #     sequence_values={
#     #         "distractor_text": "Left\nLeft\nLeft",
#     #         "target_text": "Right",
#     #         "correct_key": "g",
#     #     },
#     #     window_settings={"units": "pix"}
#     # )
