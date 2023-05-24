from io import BytesIO
from ftplib import FTP
from dotenv import load_dotenv
import os
load_dotenv()

ftp = FTP(os.environ["FTP_SERVER_URL"])
ftp.login(os.environ["FTP_LOGIN"], os.environ["FTP_PASS"])

from aiohttp import web
import socketio
import base64

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)


@sio.event
async def getThList(sid):
    await sio.emit("thList", ftp.nlst(os.environ["FTP_THUMBS_PATH"]))

@sio.event
async def getTh(sid, message):
    flo = BytesIO()
    ftp.retrbinary("RETR "+os.environ["FTP_THUMBS_PATH"]+message, flo.write)

    img = message.split(".")
    await sio.emit("th", {"bytes": base64.b64encode(flo.getvalue()).decode(), "name": img[0][3:], "ext": img[1]})

@sio.event
async def getImg(sid, message):
    flo = BytesIO()
    ftp.retrbinary("RETR "+os.environ["FTP_IMAGES_PATH"]+message["name"]+"."+message["ext"], flo.write)

    await sio.emit("img", base64.b64encode(flo.getvalue()).decode())

if __name__ == '__main__':
    web.run_app(app, port=int(os.environ["FTP_SERVER_PORT"]))