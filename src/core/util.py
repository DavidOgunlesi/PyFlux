from pathlib import Path


def GetRootPathDir():
    '''
    Returns the root path of the project
    '''
    return Path(__file__).parent.parent.parent