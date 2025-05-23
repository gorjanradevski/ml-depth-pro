import pyrealsense2 as rs

ctx = rs.context()
devices = ctx.query_devices()
if devices:
    print("Devices detected:")
    for dev in devices:
        print(dev.get_info(rs.camera_info.name))
else:
    print("No RealSense device found.")

