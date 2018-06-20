if __name__ == '__main__':
    with open('speed_test_results') as _file:
        total = 0
        count = 0
        for line in _file:
            total += float(line)
            count += 1
    with open('ave_speed.py', 'w') as _file:
        _file.write('AVE_SPEED = {}\n'.format((total/count)/5))
