from machine import Pin
import urequests
import json
import time

def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect("", "") # network name, network password
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())


def send_slack_alert():
    url = '' # slack webhook url
    payload = '{"text": "You have a visitor!"}'
    urequests.request("POST", url, data=payload)


def any_lights_on(url):
    data = urequests.request("GET", url)
    lights = json.loads(data.text)
    data.close() # important to close connection

    for name, state in lights.items():
      if state['state']['on']:
        return True

    return False


def set_lights(url, on):
    data = urequests.request("GET", url)
    lights = json.loads(data.text)
    data.close()

    if on:
      data='{"on":true, "bri":254}'
    else:
      data='{"on":false}'

    for name in lights.keys():
      r = urequests.request("PUT", url + "/" + name + "/state", data=data)
      r.close()
      

def toggle_lights():
    url = ''

    if any_lights_on(url):
      set_lights(url, False)
    else:
      set_lights(url, True)

do_connect()

btn_pressed = False
btn = Pin(14, Pin.IN, Pin.PULL_UP)
while True:
    if not btn.value() and not btn_pressed:
        btn_pressed = True
        toggle_lights()
        time.sleep(.2)
    elif btn.value() and btn_pressed:
        btn_pressed = False
