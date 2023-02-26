from components.coral import CoralInterpreter
from PIL import Image
import numpy as np

model = CoralInterpreter("models/model_quantized2_edgetpu.tflite")
print("Loaded the interpreter")

image = np.array(Image.open("data/sample.png"))
image = image[...,:3]
print("Loaded the image")

output_data = model.infer(image)
print("Ran the inference")

output = np.argmax(output_data[0], axis=-1)
output = (output*255/7).astype("uint8")
print("Transformed the output")

output_image = Image.fromarray(output, mode="L")
output_image.save("data/sample_output.png")
print("Saved the output")
