start_screen_text = """
Welcome to this test experiment. Right now you are looking at a Static Information Screen. \
This is to provide you with some information about this experiment and what you should know before starting.

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam venenatis accumsan eros a vehicula. Quisque mollis \
ante ac leo tempus egestas ut vitae lectus. Suspendisse maximus venenatis tortor, in imperdiet ipsum rutrum quis. \
Nulla quis est in mauris feugiat cursus feugiat nec tellus. Quisque a purus iaculis, commodo nibh id, pharetra odio. \
Sed sit amet ligula a diam placerat imperdiet. Fusce in quam vehicula odio pharetra maximus. Aliquam eget nunc sollicitudin, \
fermentum ipsum bibendum, convallis nisl. In nec eros turpis. Donec et ultricies quam. Etiam ipsum erat, consequat et \
bibendum id, eleifend sit amet est. Curabitur sit amet tincidunt ante, at congue orci.

Press [space] to continue.
"""

start_screen = {
    "type": "Screen",
    "visual_components": [
        {
            "name": "text",
            "type": "TextStim",
            "spec": {
                "color": "white",
                "height": 32,
                "wrapWidth": 1200,
                "text": start_screen_text,
            },
        }
    ],
    "response": {"keys": ["space"]},
}

if __name__ == "__main__":
    from conflict_task.preview import preview_sequence

    preview_sequence(start_screen)
