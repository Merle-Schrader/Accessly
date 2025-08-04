

def add_option(option, args=None):
    if type(option) != str:
        raise TypeError('Accessibility keyword should be a string!')
    try:
        file = __import__('accessibilities.access_' + option)
        file.run(args)
    except:
        raise ValueError('Could not find "' + option + '" in the accessibility options. Please consider adding it!')

