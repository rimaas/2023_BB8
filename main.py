#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, Motor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.led import Leds
from ev3dev2.sound import Sound

ts = TouchSensor()
leds = Leds()

print("Press the touch sensor to change the LED color!")

while True:
    if ts.is_pressed:
        leds.set_color("LEFT", "GREEN")
        leds.set_color("RIGHT", "GREEN")
        sound = Sound()
        sound.speak('Hallo Floris en Sanne, jullie zijn lief')

        m1 = LargeMotor(OUTPUT_A)
        m1.on_for_rotations(SpeedPercent(100), 5)
        m2 = LargeMotor(OUTPUT_B)
        m2.on_for_rotations(SpeedPercent(100), 5)
        m3 = Motor(OUTPUT_C)
        m3.on_for_rotations(SpeedPercent(100), 5)
        m4 = Motor(OUTPUT_D)
        m4.on_for_rotations(SpeedPercent(100), 5)

    else:
        leds.set_color("LEFT", "RED")
        leds.set_color("RIGHT", "RED")
