import route

if __name__ == '__main__':
    print("Here we go.")
    control = route.RouteControl()
    print("Adding route point.")
    control.add_point(0, 0)
    print("Starting")
    control.start()
