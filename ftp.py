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
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import jwt

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)


authSid = ""
@sio.event
async def authorize(sid, token):
    try:
        public_key = open(os.environ["RSA_PATH"], "r").read()
        key = serialization.load_ssh_public_key(public_key.encode(), default_backend())

        jwt.decode(token, key, algorithms=[jwt.get_unverified_header(token)["alg"], ])
        
        global authSid
        authSid = sid
    except Exception as error:
        print("error", error)
        await sio.disconnect(sid)


@sio.event
async def getThList(sid):
    if(authSid == sid):
        await sio.emit("thList", ftp.nlst(os.environ["FTP_THUMBS_PATH"]))
    else:
        await sio.disconnect(sid)

@sio.event
async def getTh(sid, message):
    if(authSid == sid):
        flo = BytesIO()
        ftp.retrbinary("RETR "+os.environ["FTP_THUMBS_PATH"]+message, flo.write)

        img = message.split(".")
        await sio.emit("th", {"bytes": base64.b64encode(flo.getvalue()).decode(), "name": img[0][3:], "ext": img[1]})
    else:
        await sio.disconnect(sid)

@sio.event
async def getImg(sid, message):
    if(authSid == sid):
        flo = BytesIO()
        ftp.retrbinary("RETR "+os.environ["FTP_IMAGES_PATH"]+message["name"]+"."+message["ext"], flo.write)

        await sio.emit("img", base64.b64encode(flo.getvalue()).decode())
    else:
        await sio.disconnect(sid)


if __name__ == '__main__':
    web.run_app(app, port=int(os.environ["FTP_SERVER_PORT"]))