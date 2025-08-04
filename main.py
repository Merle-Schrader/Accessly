def add_options(options, **kwargs):
    """
    Args:
    
    options (str or list): list of strings containing accessibility features to be applied

    **kwargs: keyword arguments for each of the accessibility options

    """

    # If there is only one option:
    if type(options) == str:
        try:
            file = __import__('accessibilities.access_' + options)
            file.apply(kwargs[options])
        except:
            raise ValueError('Could not find "' + options + '" in the accessibility options. Please consider adding it!')

    # If there are multiple options:
    if type(options) != list:
        raise TypeError('Accessibility options should be a string or a list of strings!')
    for option in options:
        if type(option) != str:
            raise TypeError('Accessibility options should be a list of strings!')
    for option in options:
        try:
            file = __import__('accessibilities.access_' + option)
            file.apply(kwargs[option])
        except:
            raise ValueError('Could not find "' + option + '" in the accessibility options. Please consider adding it!')

