from pyinfra.api import FactBase

from .util.packaging import parse_packages

BREW_REGEX = r'^([a-zA-Z0-9\-]+)\s([0-9\._+a-z\-]+)'


class BrewPackages(FactBase):
    '''
    Returns a dict of installed brew packages:

    .. code:: python

        'package_name': ['version'],
        ...
    '''

    command = 'brew list --versions'
    default = dict
    use_default_on_error = True

    def process(self, output):
        return parse_packages(BREW_REGEX, output)


class BrewCasks(BrewPackages):
    '''
    Returns a dict of installed brew casks:

    .. code:: python

        'package_name': ['version'],
        ...
    '''

    command = 'brew cask list --versions'


class BrewTaps(FactBase):
    '''
    Returns a list of brew taps.
    '''

    command = 'brew tap'
    default = list
    use_default_on_error = True

    def process(self, output):
        return output
