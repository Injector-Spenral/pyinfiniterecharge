#!/usr/bin/env python3

# Copyright (c) 2017-2018 FIRST. All Rights Reserved.
# Open Source Software - may be modified and shared by FRC teams. The code
# must be accompanied by the FIRST BSD license file in the root directory of
# the project.

import wpilib
import rev
import rev.color

import magicbot

from controllers.indexer_controller import IndexerController
from controllers.shooter_controller import ShooterController
from controllers.spinner import SpinnerController
from components.indexer import Indexer
from components.shooter import Shooter
from components.spinner import Spinner


class MyRobot(magicbot.MagicRobot):
    indexer_controller: IndexerController
    shooter_controller: ShooterController
    spinner_controller: SpinnerController
    indexer: Indexer
    shooter: Shooter
    spinner: Spinner

    def createObjects(self) -> None:
        """Robot initialization function"""
        # object that handles basic drive operations
        self.joystick_left = wpilib.Joystick(0)
        self.joystick_right = wpilib.Joystick(1)
        self.spinner_joystick = wpilib.Joystick(2)

        self.shooter_outer_motor = rev.CANSparkMax(3, rev.MotorType.kBrushless)
        self.shooter_centre_motor = rev.CANSparkMax(2, rev.MotorType.kBrushless)

        self.loading_piston = wpilib.Solenoid(0)

        self.indexer_motors = [wpilib.Spark(1), wpilib.Spark(0)]
        self.indexer_switches = [wpilib.DigitalInput(8), wpilib.DigitalInput(9)]

        self.spinner_motor = wpilib.Spark(2)
        self.spinner_solenoid = wpilib.DoubleSolenoid(2, 3)
        self.colour_sensor = rev.color.ColorSensorV3(wpilib.I2C.Port.kOnboard)

    def teleopInit(self) -> None:
        """Executed at the start of teleop mode"""

    def teleopPeriodic(self) -> None:
        """Executed every cycle"""
        self.handle_shooter_inputs(self.joystick_left)
        self.handle_indexer_inputs(self.joystick_left)
        self.handle_spinner_inputs(self.spinner_joystick)
        self.send_shooter_values()

    def handle_shooter_inputs(self, joystick: wpilib.Joystick) -> None:
        if joystick.getRawButtonPressed(7):
            self.shooter_controller.centre_rpm_constant -= 100
        if joystick.getRawButtonPressed(8):
            self.shooter_controller.centre_rpm_constant += 100
        if joystick.getRawButtonPressed(9):
            self.shooter_controller.outer_rpm_constant -= 100
        if joystick.getRawButtonPressed(10):
            self.shooter_controller.outer_rpm_constant += 100
        if joystick.getRawButtonPressed(11):
            self.shooter_controller.fire()
        if joystick.getRawButtonPressed(12):
            self.shooter_controller.toggle_constant()
        self.shooter_controller.set_motors(
            self.joystick_left.getThrottle(), self.joystick_right.getThrottle()
        )

    def handle_indexer_inputs(self, joystick: wpilib.Joystick) -> None:
        if joystick.getTrigger():
            # self.indexer_controller.next_state("eject_cells")
            self.indexer_controller.state = "eject_cells"
        if joystick.getRawButtonPressed(3):
            # self.indexer_controller.next_state("shoot_cells")
            self.indexer_controller.state = "shoot_cells"
        if joystick.getRawButtonPressed(4):
            # self.indexer_controller.next_state("intake_cells")
            self.indexer_controller.state = "intake_cells"

    def handle_spinner_inputs(self, joystick: wpilib.Joystick) -> None:
        if joystick.getRawButtonPressed(7):
            self.spinner_controller.run(test=True, task="position")
            print(f"Spinner Running")
        if joystick.getRawButtonPressed(9):
            self.spinner.piston_up()
            print("Spinner Piston Up")
        if joystick.getRawButtonPressed(10):
            self.spinner.piston_down()
            print("Spinner Piston Down")
        if joystick.getRawButtonPressed(8):
            print(f"Detected Colour: {self.spinner_controller.get_current_colour()}")
            print(f"Distance: {self.spinner_controller.get_wheel_dist()}")

    def send_shooter_values(self) -> None:
        wpilib.SmartDashboard.putNumber(
            "outerError", self.shooter_controller.get_outer_error()
        )
        wpilib.SmartDashboard.putNumber(
            "centreError", self.shooter_controller.get_centre_error()
        )

        wpilib.SmartDashboard.putNumber(
            "outerVelocity", self.shooter_controller.outer_throttle
        )
        wpilib.SmartDashboard.putNumber(
            "centreVelocity", self.shooter_controller.centre_throttle
        )


if __name__ == "__main__":
    wpilib.run(MyRobot)
