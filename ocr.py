from PIL import Image
import sys
from pyocr.builders import TextBuilder
from pyocr.pyocr import get_available_tools, TOOLS

tools = get_available_tools()
if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)

tool = tools[0]
print("Will use tool '%s'" % (tool.get_name()))

txt = tool.image_to_string(
    Image.open("./image_file/test_1_5_01.png"),
    lang="jpn",
    builder=TextBuilder(tesseract_layout=6)
)

print(txt)