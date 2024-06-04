
# # 获取资源文件的绝对路径
# def resource_path(relative_path):
#     #print(os.getcwd())
#     #print(os.path.join(sys._MEIPASS, relative_path))
#     print(os.path.join(os.path.abspath("."), relative_path))
#     if hasattr(sys, '_MEIPASS'):
#         return os.path.join(sys._MEIPASS, relative_path)
#     return os.path.join(os.path.abspath("."), relative_path)

# img_device_base = resource_path('/assets/base.png')
# img_device_microscope = resource_path('/assets/microscope.png')
# img_device_micrometer_drum = resource_path('/assets/micrometer_drum.png')
# img_device_reflector = resource_path('/assets/reflector.png')

img_device_base = '/assets/base.png'
img_device_microscope = '/assets/microscope.png'
img_device_micrometer_drum = '/assets/micrometer_drum.png'
img_device_reflector = '/assets/reflector.png'
vid_device = '/assets/device.mp4'
img_cover = '/assets/cover.jpg'
img_principle_geomatric = '/assets/principle_geomatric.png'
img_principle_light_path = '/assets/principle_light_path.png'
img_principle_rings_pattern = '/assets/principle_rings_pattern.png'