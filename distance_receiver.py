from VLC.device import Device

if __name__ == "__main__":
    d = Device()

    message = ""
    while True:  # while not terminated
        d.listen()
