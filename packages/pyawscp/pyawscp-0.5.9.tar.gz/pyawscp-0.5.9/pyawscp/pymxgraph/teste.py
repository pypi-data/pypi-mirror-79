from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

drawing = svg2rlg("D:/Downloads/home.html")
renderPM.drawToFile(drawing, "D:/Downloads/file.png", fmt="PNG")