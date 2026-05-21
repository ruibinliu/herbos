from herbos.core.log import logger

socketio = None

def init_events(sio):
    global socketio
    socketio = sio


def emit_log(message):
    if socketio:
        socketio.emit("log", {"message": message})
    logger.info(message)

def emit_status(**kwargs):
    if socketio:
        socketio.emit("status", kwargs)
    logger.info(kwargs)
