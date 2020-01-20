import wpilib
import rev

from magicbot import tunable


class Shooter:
    outer_motor: rev.CANSparkMax
    centre_motor: rev.CANSparkMax
    loading_piston: wpilib.DoubleSolenoid

    # outer_rpm = tunable(0)
    # centre_rpm = tunable(0)
    def __init__(self):
        self.outer_rpm = 4400
        self.centre_rpm = -3700

    def on_enable(self) -> None:
        self.centre_motor.stopMotor()
        self.outer_motor.stopMotor()

    def setup(self) -> None:
        self.outer_motor.setIdleMode(rev.CANSparkMax.IdleMode.kCoast)
        self.centre_motor.setIdleMode(rev.CANSparkMax.IdleMode.kCoast)

        self.outer_encoder = self.outer_motor.getEncoder()
        self.centre_encoder = self.centre_motor.getEncoder()

        self.centre_pid = self.centre_motor.getPIDController()
        self.outer_pid = self.outer_motor.getPIDController()

        self.centre_pid.setP(4e-4)
        self.centre_pid.setI(0)
        self.centre_pid.setD(0)
        self.centre_pid.setFF(0.000156)

        self.outer_pid.setP(4.77e-4)
        self.outer_pid.setI(0)
        self.outer_pid.setD(0)
        self.outer_pid.setFF(0.000156)

    def execute(self) -> None:
        # self.outer_rpm = 0
        # self.centre_rpm = 0
        self.centre_pid.setReference(self.centre_rpm, rev.ControlType.kVelocity)
        self.outer_pid.setReference(self.outer_rpm, rev.ControlType.kVelocity)

    def get_centre_error(self) -> float:
        return self.centre_rpm - self.centre_encoder.getVelocity()

    def get_outer_error(self) -> float:
        return self.outer_rpm - self.outer_encoder.getVelocity()

    def set_motor_rpm(self, v_outer, v_centre) -> None:
        self.centre_rpm = v_centre
        self.outer_rpm = v_outer

