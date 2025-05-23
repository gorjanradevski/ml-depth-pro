import cv2
import numpy as np

# Load the depth image (16-bit)
depth_image_path = "saved_images/409592125011600_depth.png"  # Replace this with the path to your depth image
depth_image = cv2.imread(depth_image_path, cv2.IMREAD_UNCHANGED)

if depth_image is None:
    print("Error: Depth image could not be loaded!")
    exit()

# Move all pixels with unknown depth (=0) to 10000mm
depth_image[depth_image == 0] = 10000

# Normalize the depth image to a range of 0-255 for color mapping
# Convert to 8-bit by scaling the values (depth range is 16-bit, usually up to 65535)
depth_normalized = cv2.convertScaleAbs(depth_image, alpha=0.03)  # Adjust alpha for better scaling if needed

# Apply a color map to the depth image for better visualization
depth_colormap = cv2.applyColorMap(depth_normalized, cv2.COLORMAP_JET)

# Callback function for mouse click event
def on_mouse(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE or event == cv2.EVENT_LBUTTONDOWN:
        # Get the depth at the chosen pixel (in mm)
        depth_at_pixel = depth_image[y, x]
        
        # Print the depth in millimeters in the terminal (optional: display in GUI)
        print(f"Pixel ({x},{y}) - Depth: {depth_at_pixel} mm")
        
        # Display the depth on the image as text (optional)
        image_copy = depth_image.copy()
        cv2.putText(image_copy, f"Depth: {depth_at_pixel} mm", (x + 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# Display the depth image and use the callback function
cv2.imshow("Depth Image", depth_colormap)
cv2.setMouseCallback("Depth Image", on_mouse)

# Wait for a key press to close the window
cv2.waitKey(0)
cv2.destroyAllWindows()
