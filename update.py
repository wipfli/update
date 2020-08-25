def get_cmdline(path='/proc/cmdline'):
    cmdline = ''
    # ...
    cmdline = 'mmclbk0p3'
    return cmdline

def get_passive(cmdline, p2='mmclbk0p2', p3='mmclbk0p3'):
    if p2 in cmdline:
        return p3
    if p3 in cmdline:
        return p2
    return None

def mount_passive(parition='mmclbk0p2', path='/mnt/passive'):
    success = False
    # ...
    return success

def get_current_version():
    current_version = ''
    # ...
    current_version = '1.0.0'
    return current_version

def get_latest_version(url, beta=False):
    latest_version = ''
    # ...
    return latest_version