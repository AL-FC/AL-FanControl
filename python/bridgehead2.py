import serial

import asyncio
from asyncio import sleep

console = serial.Serial('/dev/ttyACM0', 9600)


@asyncio.coroutine
def reader(console):
    while True:
        response = ''
        character = ''
        while character != '\n':
            print('reading')
            character = console.read().decode('ASCII')
            print('read')
            response += character
            print(character)
        print(response)
        sleep(1)


@asyncio.coroutine
def writer(console):
    while True:
        message = '123;123;123'
        print('writing')
        console.writelines([message.encode('ASCII')])
        print('written')
        sleep(1)


loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait([writer(console), reader(console)]))
loop.close()
