import route
import time

if __name__ == '__main__':
    try:
        print("Here we go.")
        control = route.RouteControl()
        print("Adding route point.")
        control.add_point(30, 0)
        print("{} {}".format(control.route, control.route[0].distance))
        print("Starting")
        control.start()
        while (True):
            time.sleep(5)
    except KeyboardInterrupt:
        pass
    finally:
        control.stop()
