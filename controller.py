import asyncio
from ulid import ULID
from sanic import Request, Sanic
from sanic.response import html
from sanic.log import logger
from sanic_ext import Extend
from datastar_py.sanic import datastar_respond
from datastar_py.sse import ServerSentEventGenerator as SSE
from htpy import html as root, body, main, div, head, pre, span
from rendering_and_head import ds_script
from view import base


app = Sanic("HelloWorldApp")
app.config.CORS_ORIGINS = "http://localhost"
Extend(app)
app.ctx.client_queues = {}


@app.middleware("request")
async def identify_session(request):
    session_id = request.ctx.session_id = request.cookies.get("id", "no_sid")
    if session_id == "no_sid":
        request.ctx.session_id = str(ULID())


@app.middleware("response")
async def ensure_session_id_cookie(request, response):
    session_id_cookie = request.cookies.get("id", "no_sid")
    if request.ctx.session_id != session_id_cookie:
        logger.info(f"New session created: {request.ctx.session_id}")
        response.add_cookie("id", request.ctx.session_id)


@app.get("/")
async def index(request):
    return html(base())


@app.signal("todo_app.todo.created")
async def log_to_console(**ctx):
    logger.info(f"New todo created: {ctx}")


@app.signal("todo_app.user.<connections_changed>")
async def connections_changed(**ctx):
    usercount = len(app.ctx.client_queues)
    update = SSE.merge_signals({"usercount": usercount})
    tasks = [
        client_queue.put(update) for client_queue in app.ctx.client_queues.values()
    ]
    if tasks:
        await asyncio.gather(*tasks)


@app.get("/updates")
async def updates(request: Request):
    sse_response = await datastar_respond(request)
    session_id = request.ctx.session_id or "anonymous"
    client_queues = app.ctx.client_queues or {}
    client_queue = app.ctx.client_queues[session_id] = asyncio.Queue()
    await app.dispatch("todo_app.user.connected", context={"session_id": session_id})

    try:
        while True:
            event_data = await client_queue.get()
            await sse_response.send(event_data)
            client_queue.task_done()
    except asyncio.CancelledError:
        logger.info("Client disconnected (SSE stream cancelled.")
    except Exception as e:
        logger.error(f"SSE stream error: {e}", exc_info=True)
    finally:
        try:
            del client_queues[session_id]
            logger.info(
                f"Client cleanup finished. Remaining clients: {len(app.ctx.client_queues)}."
            )
        except KeyError:
            logger.warning(
                "Attempted to remove a client queue that was not in ctx.client_queues"
            )
        except Exception as e:
            logger.error(f"An error ocurred while trying to cleanup a connection: {e}")

        await app.dispatch(
            "todo_app.user.disconnected", context={"session_id": request.ctx.session_id}
        )
