from machine import Pin
import urequests
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


do_connect()

btn_pressed = False
btn = Pin(14, Pin.IN, Pin.PULL_UP)
while True:
    if not btn.value() and not btn_pressed:
        btn_pressed = True
        send_slack_alert()
        time.sleep(.2)
    elif btn.value() and btn_pressed:
        btn_pressed = False
