# FTPimageViewer-Server

### packages
```
pip3 install python-dotenv
pip3 install pyjwt[crypto]
```

## .env example
```
FTP_SERVER_URL = 98.765.432.10
FTP_SERVER_PORT = 3000
FTP_LOGIN = login
FTP_PASS = password

FTP_THUMBS_PATH = user/thumbnails/
FTP_IMAGES_PATH = user/images/

RSA_PATH = .ssh/id_rsa.pub
```

## generete rsa
```
mkdir .ssh
ssh-keygen -t rsa -f ".ssh/id_rsa"
```