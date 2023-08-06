import requests
import sys
import json
from time import sleep
port = None
host = None
def send(data):
  port = get_port()
  host = get_host()
  if (host is None):
    host = '127.0.0.1'
  requests.post(host + ':' + port + '/test', data = data)
  
def get_print():
  sleep(200)
  port = get_port()
  host = get_host()
  if (host is None):
    host = '127.0.0.1'
  r = requests.get(host + ':' + port + '/test')
  if r.status_code == 200:
    try:
      info = json.loads(r.text)
      if info.get('status') == 1:
        return []
      return info.get('msg')
    except Exception as e:
      print(e)
      return []
      
  
def get_port():
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

def get_host():
  global host
  if (host != None):
    return host
  match = False
  for i in sys.argv:
    if match:
      host = i
      break;
    if i == '--host':
      match = True
  return host

def pass_test(msg):
  send({ 'status': 0, 'msg': msg })
  
def no_pass_test(msg):
  send({ 'status': 1, 'msg': msg })