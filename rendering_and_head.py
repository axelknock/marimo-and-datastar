# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "htpy==25.6.2",
#     "marimo",
#     "wigglystuff==0.1.14",
# ]
# ///

import marimo

__generated_with = "0.13.15"
app = marimo.App(width="columns", html_head_file="head.html")

with app.setup:
    # Initialization code that runs before all other cells
    import htpy
    from htpy import script, Element, VoidElement, div, input, output
    import marimo as mo


@app.function
def setup_rendering():
    def render(self):
        return mo.Html(self.__html__())

    Element._display_ = render
    VoidElement._display_ = render


@app.cell
def _():
    setup_rendering()
    return


@app.cell(hide_code=True)
def _():
    mo.md(
        """
    ```
    <input data-bind-input />
    <div data-text="$input">
      I will be replaced with the contents of the input signal
    </div>
    ```
    """
    )
    return


@app.function
def ds_script():
    return script(
        type="module",
        src="https://cdn.jsdelivr.net/gh/starfederation/datastar@1.0.0-beta.11/bundles/datastar.js",
    )


@app.cell
def _(text_size):
    # HTPY div
    div(style=f"font-size: {text_size.value}rem")["Hello world"]
    return


@app.cell
def _():
    # Plain text div
    mo.Html(f"""<div>Hello world</div>""")
    return


@app.cell
def _():
    text_size = mo.ui.slider(start=1, stop=5)
    text_size
    return (text_size,)


@app.cell
def _():
    ds_script()
    return


@app.function
def create_head():
    with open("head.html", "w") as f:
        f.write(ds_script().__html__())

    with open("head.html", "r") as f:
        contents = f.read()
        print(contents)


@app.cell
def _():
    create_head()
    return


if __name__ == "__main__":
    app.run()
