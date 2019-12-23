# Kitronik Line following buggy

# Motor control
#   Motor1      Motor2      function
#   P8  P12     P0  P16
#   0   0       0   0       Coast
#   1   0       1   0       Forward
#   0   1       0   1       Reverse
#   1   1       1   1       Brake

from microbit import *
import radio

radio.on()
started = False

def drive(onTime, offTime):
    global started
    stop(0)
    while True:
        incoming = radio.receive()
        if incoming is not None:
            # display.show(incoming)
            uart.write('Received: "' + incoming + '"\n')
            words = incoming.split(' ')
            if len(words) >= 2 and words[0] == 'buggy':
                if words[1] == 'start':
                    started = True
                elif words[1] == 'stop':
                    started = False
                    stop(0)
                elif len(words) == 4 and words[1] == 'direction' and started:
                    x = words[2]
                    y = words[3]
                    # uart.write('x=' + x + ' y=' + y + '\n')
                    xf = float(x)
                    yf = float(y)
                    if yf < 1:
                        if xf < 1:
                            leftforward(int(abs(yf-2)*onTime), offTime)
                        elif xf > 3:
                            rightforward(int(abs(yf-2)*onTime), offTime)
                        else:
                            forward(int(abs(yf-2)*onTime), offTime)
                    elif yf > 3:
                        if xf < 1:
                            leftbackward(int(abs(yf-2)*onTime), offTime)
                        elif xf > 3:
                            rightbackward(int(abs(yf-2)*onTime), offTime)
                        else:
                            backward(int(abs(yf-2)*onTime), offTime)
                    else:
                        stop(onTime)

################################
def forward(onTime, offTime):
    display.show(Image.ARROW_N)
    pin8.write_digital(0)
    pin12.write_digital(1)
    pin0.write_digital(0)
    pin16.write_digital(1)
    sleep(onTime)
    coast(offTime)
################################
def backward(onTime, offTime):
    display.show(Image.ARROW_S)
    pin8.write_digital(1)
    pin12.write_digital(0)
    pin0.write_digital(1)
    pin16.write_digital(0)
    sleep(onTime)
    coast(offTime)
################################
def leftforward(onTime, offTime):
    display.show(Image.ARROW_NW)
    pin8.write_digital(0)
    pin12.write_digital(1)
    pin0.write_digital(0)
    pin16.write_digital(0)
    sleep(onTime)
    coast(offTime)
################################
def rightforward(onTime, offTime):
    display.show(Image.ARROW_NE)
    pin8.write_digital(0)
    pin12.write_digital(0)
    pin0.write_digital(0)
    pin16.write_digital(1)
    sleep(onTime)
    coast(offTime)
################################
def leftbackward(onTime, offTime):
    display.show(Image.ARROW_SW)
    pin8.write_digital(1)
    pin12.write_digital(0)
    pin0.write_digital(0)
    pin16.write_digital(0)
    sleep(onTime)
    coast(offTime)
################################
def rightbackward(onTime, offTime):
    display.show(Image.ARROW_SE)
    pin8.write_digital(0)
    pin12.write_digital(0)
    pin0.write_digital(1)
    pin16.write_digital(0)
    sleep(onTime)
    coast(offTime)
################################
def coast(offTime):
    pin8.write_digital(0)
    pin12.write_digital(0)
    pin0.write_digital(0)
    pin16.write_digital(0)
    sleep(offTime)
################################
def stop(offTime):
    display.clear()
    coast(offTime)
################################
drive(100, 5)