from pycoral.utils import edgetpu
from pycoral.adapters import common

class CoralInterpreter:
    def __init__(self, model_path):
        self.model_path = model_path
        self.interpreter = edgetpu.make_interpreter(self.model_path)
        self.interpreter.allocate_tensors()

    def __enter__(self):
        return self

    def infer(self, input):
        common.set_input(self.interpreter, input)
        self.interpreter.invoke()

        output_details = self.interpreter.get_output_details()
        output_data = self.interpreter.get_tensor(output_details[0]["index"])
        return output_data