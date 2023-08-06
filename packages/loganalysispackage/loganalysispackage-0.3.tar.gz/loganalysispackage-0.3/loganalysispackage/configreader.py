import configparser


def dataconfigread(filePath):
    config = configparser.ConfigParser(interpolation=None)
    config.read(filePath)
    return config
