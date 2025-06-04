# Marimo and Datastar

This is a small demonstration of a few concepts. Namely:

 - Rendering htpy directly inside marimo as html
 - Making use of marimo's ability to import javascript libraries to bring in datastar
 - Using datastar to create reactive signals on the frontend and backend
 - Using marimo's interactive input widgets to change the rendered html
 - Using an eventbus on the backend (sanic) to keep all client state in sync

Setup with [uv](https://docs.astral.sh/uv/):

```sh
uv sync
```

Start marimo notebook:

```sh
marimo edit
```

You will see both `view.py` and `rendering_and_head.py` from marimo.

To start the backend server:

```sh
sanic controller -d
```

The `-d` flag enables automatic restart on file change.

Created with [marimo](https://marimo.io/), [datastar](https://data-star.dev/), [htpy](https://htpy.dev/), and [sanic](https://sanic.dev/en/).
