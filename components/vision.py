from networktables import NetworkTables


class Vision:
    def __init__(self) -> None:
        self.nt = NetworkTables.getTable("/vision")
        self.vision_data_entry = self.nt.getEntry("/vision/vision")
        self.vision_state_entry = self.nt.getEntry("/vision/fiducial_x")

    def on_enable(self) -> None:
        pass

    def setup(self) -> None:
        pass

    def execute(self) -> None:
        pass

    @property
    def data(self) -> float:
        return self.vision_data_entry.getDouble(0.0)

    @vision_state.setter
    def vision_state(self, value: str) -> None:
        self.vision_state_entry.setString(value)
