FONT_FAMILY = "Courier New"


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
        "response": {"keys": ["space"]},
        "early_quit_keys": ["f12"],
    }


welcome_screen_text = """
Herzlich Willkommen bei unserem Experiment! 

Vielen Dank für Ihre Teilnahme.

Um weiterzugehen, bitte Leertaste drücken 
"""

instructions1_text = """
Im folgenden Experiment werden Ihnen in jedem Durchgang zuerst drei Wörter untereinander präsentiert. Danach wird ein einzelnes Wort präsentiert. Reagieren sie nur auf dieses eine Wort.

Mögliche Wörter, die erscheinen können, sind: 
Links, Rechts, Oben, Unten 

Weiter mit Leertaste
"""

instructions2_text = """
Bitte reagieren Sie auf das einzeln präsentierte Wort wie folgt:
 
Für
Links -> F-Taste
Rechts -> G-Taste
Oben -> J-Taste
Unten -> N-Taste

Weiter mit Leertaste
"""

instructions3_text = """
Sie werden zunächst eine Übungsblock bearbeiten, um sich mit der Aufgabe vertraut zu machen. 
Danach folgen acht Experimentalblöcke.
Zwischen den einzelnen Blöcken haben Sie immer die Möglichkeit, eine kurze Pause zu machen.

Weiter mit Leertaste
"""

instructions4_text = """
Sollten während des Experiments Probleme oder Fragen auftauchen, wenden Sie sich bitte an den/die Versuchsleiter/in.

Wenn Sie bereit sind, starten Sie den Übungsblock mit der Leertaste
"""

pre_trial = [
    text_stim("welcome_screen", welcome_screen_text, 72),
    text_stim("instructions1", instructions1_text, 64),
    text_stim("instructions2", instructions2_text, 64),
    text_stim("instructions3", instructions3_text, 64),
    text_stim("instructions4", instructions4_text, 64),
]

if __name__ == "__main__":
    from conflict_task.preview import preview_sequence

    for pre in pre_trial:
        preview_sequence(pre)
