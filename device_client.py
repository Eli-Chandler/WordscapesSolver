import cv2

class Device():
    def __init__(self):
        from ppadb.client import Client as AdbClient

        client = AdbClient(host="127.0.0.1", port=5037)
        devices = client.devices()
        d = devices[0]
        self.d = d
    def swipe(self, *coords):
        command = '\n'.join([f'input {coord[0]} {coord[1]} & \\' if i != len(coords)-1 else f'input {coord[0]} {coord[1]}' for i, coord in enumerate(coords)])
        self.d.shell(command)

    def get_screen(self):
        result = self.d.screencap()
        with open('screen.png', 'wb') as fp:
            fp.write(result)
        return cv2.imread('screen.png')