import os
import sys

# Add root folder to python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PIL import Image, ImageDraw, ImageFont
from hope.offline.math_solver import solve_math_in_image

print("====================================================")
print("          PROJECT HOPE: MATH SOLVER DIAGNOSTIC      ")
print("====================================================")

# 1. Generate a mock image with equations printed on it
mock_img_path = "mock_math_problem.png"
print(f"Generating mock math problem image: {mock_img_path}")

# Create a clean white image
img = Image.new('RGB', (600, 400), color='white')
draw = ImageDraw.Draw(img)

# Load a standard Windows TrueType font at 36pt
try:
    font = ImageFont.truetype("arial.ttf", 36)
except Exception:
    font = None # Fallback

# Print equations in black text
draw.text((50, 50), "2x + 10 = 30", fill="black", font=font)
draw.text((50, 150), "12 * 5 - 15 = ", fill="black", font=font)
draw.text((50, 250), "y^2 - 16 = 0", fill="black", font=font)

# Save
img.save(mock_img_path)

# 2. Run the math solver on the generated image
print("Running solver on the image...")
results = solve_math_in_image(mock_img_path)

# 3. Print Results
print("\n========================= RESULTS =========================")
if results:
    for i, res in enumerate(results):
        print(f"[{i+1}] Type: {res['type']}")
        print(f"    Problem  : {res['problem']}")
        print(f"    Solution : {res['solution']}")
        print(f"    Original : {res['original']}\n")
else:
    print("No equations detected or solved. (If offline, ensure language/PsOcr is fully installed)")
print("===========================================================")

# Clean up
if os.path.exists(mock_img_path):
    try:
        os.remove(mock_img_path)
    except Exception:
        pass
