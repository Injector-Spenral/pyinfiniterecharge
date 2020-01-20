# from magicbot import StateMachine, state
from components.shooter import Shooter
import rev

# class ShooterController(StateMachine):
class ShooterController:
    shooter: Shooter

    def __init__(self) -> None:
        self.outer_rpm_constant = 5000
        self.centre_rpm_constant = 2200
        self.outer_rpm = 5000
        self.centre_rpm = 2200
    
    def on_enable(self) -> None:
        self.stay_constant = False

    def execute(self) -> None:
        self.centre_pid.setReference(self.centre_rpm, rev.ControlType.kVelocity)
        self.outer_pid.setReference(self.outer_rpm, rev.ControlType.kVelocity)

    def setup(self) -> None:
        self.configurePIDs()
        self.shooter.loading_piston.setPulseDuration(1)

    def configurePIDs(self) -> None:
        self.centre_pid = self.shooter.centre_motor.getPIDController()
        self.outer_pid = self.shooter.outer_motor.getPIDController()

        self.centre_pid.setP(4e-4)
        self.outer_pid.setP(4.77e-4)

        for pid in (self.centre_pid, self.outer_pid):
            pid.setI(0)
            pid.setD(0)
            pid.setFF(0.000156)

    def get_centre_error(self) -> float:
        return self.centre_rpm - self.shooter.centre_encoder.getVelocity()

    def get_outer_error(self) -> float:
        return self.outer_rpm - self.shooter.outer_encoder.getVelocity()

    def set_motor_rpm(self, v_outer: float, v_centre: float) -> None:
        self.centre_rpm = v_centre
        self.outer_rpm = v_outer
    
    def set_motors(self, outer_throttle_raw: float, centre_throttle_raw: float) -> None:
        if self.stay_constant:
            self.outer_throttle = self.outer_rpm_constant
            self.centre_throttle = self.centre_rpm_constant
        else:
            self.outer_throttle = ((-outer_throttle_raw + 1) / 2) * 5000
            self.centre_throttle = ((-centre_throttle_raw + 1) / 2) * 5000
        self.set_motor_rpm(self.outer_throttle, self.centre_throttle)

    def fire(self) -> None:
        self.shooter.loading_piston.startPulse()

    def toggle_constant(self) -> None:
        self.stay_constant = not self.stay_constant
