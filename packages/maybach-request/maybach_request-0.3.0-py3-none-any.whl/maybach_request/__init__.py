import requests
import sys
import json
from time import sleep
port = None

def send(data):
  port = getPort()
  requests.post('http://127.0.0.1:' + port + '/test', data = data)
  
def get_print():
  sleep(200)
  port = getPort()
  r = requests.get('http://127.0.0.1:' + port + '/test')
  if r.status_code == 200:
    try:
      info = json.loads(r.text)
      if info.get('status') == 1:
        return []
      return info.get('msg')
    except Exception as e:
      print(e)
      return []
      
  
def getPort():
  global port
  if (port != None):
    return port
  match = False
  for i in sys.argv:
    if match:
      port = i
      break;
    if i == '--port':
      match = True
  return port

def pass_test(msg):
  send({ 'status': 0, 'msg': msg })
  
def no_pass_test(msg):
  send({ 'status': 1, 'msg': msg })