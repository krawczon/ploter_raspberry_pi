import RPi.GPIO as GPIO
import time
import servo
from threading import Thread
import reader

class Ploter():
    def __init__(self, filename):

        self.filename = filename
        self.events = reader.reader(self.filename)

        self.x = 0
        self.y = 0
        self.draw = False
        self.rgba = (0,1,0,0.5)

        self.stepX   = 14
        self.directX = 15
        self.stepY   = 23
        self.directY = 24
        ms1x         = 25
        ms2x         = 8
        ms3x         = 7
        ms1y         = 16
        ms2y         = 20
        ms3y         = 21

        GPIO.setmode(GPIO.BCM)
        pins = [self.stepX, self.stepY, self.directX, self.directY,
                ms1x, ms2x, ms3x, ms1y, ms2y, ms3y]

        microsteps = [ms1x, ms2x, ms3x, ms1y, ms2y, ms3y]

        for pin in pins:
            GPIO.setup(pin, GPIO.OUT)

        for ms in microsteps:
            GPIO.output(ms, True)

    def mainloop(self):
        step_time = 0.0003
        current_x = 0
        current_y = 0

        for event in self.events:
            self.draw = True
            time.sleep(0.015)

            if event == 'up':
                self.pen_event(event)
            elif event == 'down':
                self.pen_event(event)

            else:
                x = int(event[0]*200)
                y = int(event[1]*200)
                self.x = x
                self.y = y

                if x - current_x < 0:
                    self.dirx = False
                else:
                    self.dirx = True
                if y - current_y < 0:
                    self.diry = True
                else:
                    self.diry = False

                steps_x = abs(x - current_x)
                steps_y = abs(y - current_y)
                current_x = x
                current_y = y

                if steps_x > steps_y and steps_y != 0:
                    step_ty = step_time*(steps_x/steps_y)
                    step_tx = step_time
                    dty = (step_ty - step_tx)*0.1
                    dtx = 0

                elif steps_x < steps_y and steps_x != 0:
                    step_tx = step_time*(steps_y/steps_x)
                    step_ty = step_time
                    dtx = (step_tx - step_ty)*0.1
                    dty = 0

                elif steps_x == steps_y:
                    step_tx = step_time
                    step_ty = step_time
                    dtx = 0
                    dty = 0

                else:
                    dtx = 0
                    dty = 0
                    step_tx = step_time
                    step_ty = step_time

                self.draw = False
                stepper_x = Thread(target = self.stepper_motor, args=[steps_x, step_tx, dtx, self.directX, self.dirx, self.stepX, ])
                stepper_y = Thread(target = self.stepper_motor, args=[steps_y, step_ty, dty, self.directX, self.dirx, self.stepY, ])
                stepper_x.start()
                stepper_y.start()
                stepper_x.join()
                stepper_y.join()

    def stepper_motor(self, steps, step_t, dt, dir_pin, direction, step_pin):
        for i in range(steps):
            GPIO.output(dir_pin, direction)
            GPIO.output(step_pin, True)
            time.sleep(step_t + dt)
            GPIO.output(step_pin, False)

    def pen_event(self, pos):
        if pos == 'up':
            self.rgba = (0,1,0,0.5)
            servo.SetAngle(0)
        if pos == 'down':
            self.rgba = (1,1,1,1)
            servo.SetAngle(15)
