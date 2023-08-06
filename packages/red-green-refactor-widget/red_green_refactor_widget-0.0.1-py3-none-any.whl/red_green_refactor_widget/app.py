from .ui import UI

class App:

    def __init__(self):
        self.ui = UI()
        self.ui.set_advance_stage_callback(self.advance_stage)
        self.apply_stage_class(RedStage)

    def run(self):
        self.ui.run()

    def apply_stage_class(self, stage_class):
        self.stage = stage_class()
        self.ui.apply_stage(self.stage)

    def advance_stage(self):
        if isinstance(self.stage, RedStage):
            self.apply_stage_class(GreenStage)
        elif isinstance(self.stage, GreenStage):
            self.apply_stage_class(RefactorStage)
        elif isinstance(self.stage, RefactorStage):
            self.apply_stage_class(RedStage)

class RedStage:

    def __init__(self):
        self.name = "RED"
        self.hint = "Write a test, watch it fail"
        self.color = "red"

class GreenStage:

    def __init__(self):
        self.name = "GREEN"
        self.hint = "Write just enough code to pass the test"
        self.color = "green"

class RefactorStage:

    def __init__(self):
        self.name = "REFACTOR"
        self.hint = "Improve the code without changing its behavior"
        self.color = "blue"
