class ANSI:
    _styles = {
        'bold': 1,
        'faint': 2,
        'italic': 3,
        'underline': 4,
        'blink': 5,
        'reverse': 7,
        'conceal': 8,
        'strike': 9,
        'bold_off': 21,
        'underline_off': 24,
        'normal': 22,
        'reset': 0,
    }

    _colors = {
        'black': 30,
        'red': 31,
        'green': 32,
        'yellow': 33,
        'blue': 34,
        'magenta': 35,
        'cyan': 36,
        'white': 37,
        'default': 39,
    }

    _bright_colors = {
        'black': 90,
        'red': 91,
        'green': 92,
        'yellow': 93,
        'blue': 94,
        'magenta': 95,
        'cyan': 96,
        'white': 97,
    }

    _backgrounds = {
        'black': 40,
        'red': 41,
        'green': 42,
        'yellow': 43,
        'blue': 44,
        'magenta': 45,
        'cyan': 46,
        'white': 47,
        'default': 49,
    }

    _bright_backgrounds = {
        'black': 100,
        'red': 101,
        'green': 102,
        'yellow': 103,
        'blue': 104,
        'magenta': 105,
        'cyan': 106,
        'white': 107,
    }

    @staticmethod
    def style(name):
        code = ANSI._styles.get(name.lower())
        if code is None:
            raise ValueError(f"Unknown style: {name}")
        return f"\33[{code}m"

    @staticmethod
    def color(name, bright=False):
        name = name.lower()
        if bright:
            code = ANSI._bright_colors.get(name)
        else:
            code = ANSI._colors.get(name)
        if code is None:
            raise ValueError(f"Unknown color: {name}")
        return f"\33[{code}m"

    @staticmethod
    def background(name, bright=False):
        name = name.lower()
        if bright:
            code = ANSI._bright_backgrounds.get(name)
        else:
            code = ANSI._backgrounds.get(name)
        if code is None:
            raise ValueError(f"Unknown background color: {name}")
        return f"\33[{code}m"

    @staticmethod
    def reset():
        return "\33[0m"