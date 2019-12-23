""" Use the accelerometer on the microbit to 
    control the movement of a buggy driven by a second microbit
    communication over radio (bluetooth)

    Left Button:  Start the buggy
    Right Button: Stop the buggy
"""
import microbit
import radio
import math

### Float display class

class FloatDisplay:

    # Array of floating point LED brightness levels (0.0=off, 1.0=on);
    # rows and columns correspond to the LEDs on the Microbit, e.g.
    # leds[0][2] maps to the second LED in the first row.
    leds = None

    def __init__(self):
        self.clear()

    def clear(self):
        """ Clear the SmartDisplay.
        """
        self.leds = [[0.0]*5 for i in range(5)]

    def display(self):
        """ Write the contents of the SmartDisplay to the
            MB image buffer and display it.

            The method applies clipping to keep the brightness
            values within the permitted range.
        """
        img_array = bytearray()
        local_int = int
        # img_array = [min(max(local_int(x * 9.0), 0), 9) for row in self.leds for x in row]
        for row in self.leds:
            for x in row:
                x = local_int(x * 9.0)
                x = min(max(x, 0), 9)
                img_array.append(x)
        img = microbit.Image(5, 5, img_array)
        microbit.display.show(img)

    def show_point(self, row, column, level=1.0, scale=1.0):
        """ This works with floating point row and column and
            interpolates the brightness.
            All other display content is cleared.
        """
        leds = self.leds
        for led_row in range(5):
            for led_column in range(5):
                # Calculate the squared distance
                # d2 = (row - led_row)**2.0 + (column - led_column)**2.0
                d2 = abs((row - led_row)) + abs((column - led_column))
                # Set brightness based on the distance to the point,
                # using scale for scaling
                leds[led_row][led_column] = level - scale * d2

###########################
def balance(sensitivity, delay):
    radio.on()
    sx, sy, sz = 0.0, 0.0, 0.0
    sensitivity = 1.0
    delay = 200
    fd = FloatDisplay()
    while True:
        ##################################
        # start / stop
        if microbit.button_a.is_pressed():
            radio.send('buggy start')
        if microbit.button_b.is_pressed():
            radio.send('buggy stop')
        ##################################
        ax, ay, az = microbit.accelerometer.get_values()
        x = (ax - sx) / 100.0 * sensitivity
        x = min(max(x+2, 0.0), 4.0)
        y = (ay - sy) / 100.0 * sensitivity
        y = min(max(y+2, 0.0), 4.0)
        z = (az - sz) / 100.0 * sensitivity
        z = min(max(z+2, 0.0), 4.0)
        # print ('x:%4f y:%4f z:%4f ax:%4i ay:%4i az:%4i speed:%4f' % (
        #        x, y, z, ax, ay, az, speed))
        ################################################
        radio.send('buggy direction ' + str(x) + ' ' + str(y))
        #
        fd.clear()
        fd.show_point(y, x, scale=0.5)
        fd.display()
        microbit.sleep(delay)


###########################
balance(10, 0)
