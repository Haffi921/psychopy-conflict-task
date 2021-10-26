def text_stim(name, text, size):
    return {
        "type": "Screen",
        "visual_components": [
            {
                "name": name,
                "type": "TextStim",
                "spec": {
                    "text": text,
                    "height": size,
                    "wrapWidth": 1500,
                    "font": FONT_FAMILY,
                    "color": "black",
                },
            }
        ],
        "response": {"keys": ["f12"]},
    }


FONT_FAMILY = "Courier New"

post_trial_text = """
Experiment beendet!
Vielen Dank für Ihre Teilnahme!

Bitte melden Sie sich bei dem/der Versuchsleiter/in, dass Sie fertig sind. 
"""

post_trial = [text_stim("post_trial", post_trial_text, 72)]

if __name__ == "__main__":
    from conflict_task.preview import preview_sequence

    for post in post_trial:
        preview_sequence(post)
