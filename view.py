# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "datastar-py==0.4.4",
#     "htpy==25.6.2",
#     "marimo",
#     "sanic==25.3.0",
#     "sanic-ext==24.12.0",
#     "wigglystuff==0.1.14",
# ]
# ///

import marimo

__generated_with = "0.13.15"
app = marimo.App(width="columns", html_head_file="head.html")

with app.setup:
    # Initialization code that runs before all other cells
    from htpy import (
        body,
        div,
        head,
        input,
        main,
        output,
        pre,
        span,
    )
    from htpy import (
        html as root,
    )
    from wigglystuff import ColorPicker

    PORT = 1337

    from rendering_and_head import ds_script, setup_rendering

    setup_rendering()


@app.function
def view(color="#000000", port=8000):
    return root[
        head[ds_script()],
        body[
            main[
                div(
                    data_on_load=f"@get('http://127.0.0.1:{port}/updates')",
                    data_signals_usercount=True,
                    style=f"color: {color}",
                )[
                    div["Connected users: ", span(data_text="$usercount")],
                    pre(data_text="ctx.signals.JSON()"),
                ],
            ]
        ],
    ]


@app.cell
def _(mo):
    text = mo.ui.text()
    mo.md(f"""Text input: {text}""")
    return (text,)


@app.cell
def _(mo, text):
    text.value
    mo.md(f"""Text output: {text.value}""")
    return


@app.cell
def _():
    div[
        div["Text input: "],
        input(data_bind_input=True, style="border: 1px solid black"),
        div["Text output: "],
        output(data_text="$input")[
            "I will be replaced with the contents of the input signal"
        ],
    ]
    return


@app.cell
def _(color_picker):
    view(color=color_picker.value["color"], port=PORT)
    return


@app.cell
def _(mo):
    color_picker = mo.ui.anywidget(ColorPicker())
    color_picker
    return (color_picker,)


@app.cell
def _():
    import marimo as mo

    return (mo,)


if __name__ == "__main__":
    app.run()
