import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18, GPIO.OUT)
pwm = GPIO.PWM(18, 50)

def SetAngle(angle):
    pwm.start(0)
    duty = angle/18 + 2
    GPIO.output(18, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.3)
    GPIO.output(18, False)
    pwm.ChangeDutyCycle(0)
