import wpilib
import rev

from magicbot import tunable


class Shooter:
    outer_motor: rev.CANSparkMax
    centre_motor: rev.CANSparkMax
    loading_piston: wpilib.Solenoid

    def __init__(self) -> None:
        pass

    def setup(self) -> None:
        self.outer_motor.setIdleMode(rev.CANSparkMax.IdleMode.kCoast)
        self.centre_motor.setIdleMode(rev.CANSparkMax.IdleMode.kCoast)

        self.outer_encoder = self.outer_motor.getEncoder()
        self.centre_encoder = self.centre_motor.getEncoder()

        self.outer_motor.setInverted(False)
        self.centre_motor.setInverted(True)

    def on_enable(self) -> None:
        self.centre_motor.stopMotor()
        self.outer_motor.stopMotor()
        self.piston_down()

    def execute(self) -> None:
        pass

    def piston_up(self) -> None:
        self.loading_piston.set(True)

    def piston_down(self) -> None:
        self.loading_piston.set(False)
