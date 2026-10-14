from classes.camera import Camera

camera = Camera(offset=(600, 400))

print(camera.syncworld_to_screen((1200, 800)))