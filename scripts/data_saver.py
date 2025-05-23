import pyrealsense2 as rs
import numpy as np
import cv2
import os

# Initialize the RealSense pipeline
pipeline = rs.pipeline()
config = rs.config()

# Configure depth and color streams
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)  # Depth stream
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)  # Color stream

# Start the pipeline
pipeline.start(config)

# Create a directory to save images
output_dir = "saved_images"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

try:
    while True:
        # Wait for a frame from the camera
        frames = pipeline.wait_for_frames()
        
        # Get the depth and color frames
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        # Skip frames if the depth frame or color frame is invalid
        if not depth_frame or not color_frame:
            continue
        
        # Convert depth frame to numpy array
        depth_image = np.asanyarray(depth_frame.get_data())
        # Convert color frame to numpy array
        color_image = np.asanyarray(color_frame.get_data())

        # Normalize the depth image to apply a color map for visualization
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

        # Display the live color and depth frames
        cv2.imshow('Live Depth Image', depth_colormap)
        cv2.imshow('Live Color Image', color_image)

        # Wait for key press
        key = cv2.waitKey(1) & 0xFF

        # If 's' is pressed, save both images
        if key == ord('s'):
            # Get the current timestamp for unique filenames
            timestamp = cv2.getTickCount()

            # Save the images in lossless PNG format
            depth_filename = os.path.join(output_dir, f"{timestamp}_depth.png")
            depth_scaled_filename = os.path.join(output_dir, f"{timestamp}_depth_scaled.png")
            color_filename = os.path.join(output_dir, f"{timestamp}_color.png")

            # Save the depth image (16-bit depth is preserved)
            cv2.imwrite(depth_filename, depth_image)
            cv2.imwrite(depth_scaled_filename, depth_colormap)

            # Save the color image (8-bit RGB)
            cv2.imwrite(color_filename, color_image)

            print(f"Saved depth and color images as {depth_filename}, {depth_scaled_filename} and {color_filename}")

        # Exit the loop when 'q' is pressed
        if key == ord('q'):
            break

finally:
    # Stop the pipeline
    pipeline.stop()
    # Close all OpenCV windows
    cv2.destroyAllWindows()
