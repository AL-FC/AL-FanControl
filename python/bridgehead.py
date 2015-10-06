from time import sleep

import serial

console = serial.Serial('/dev/ttyACM0', 9600)

while True:
    # console.write([42])

    while True:
        try:
            while console.inWaiting() == 0:
                sleep(0.1)
                print('waiting for input')
                message = '123;123;123'
                console.writelines([message.encode('ASCII')])

            response = ''
            character = ''
            while character != '\n':
                character = console.read().decode('ASCII')
                response += character
                # print(character)
            print(response)
            break
        except TypeError as e:
            print(e)
