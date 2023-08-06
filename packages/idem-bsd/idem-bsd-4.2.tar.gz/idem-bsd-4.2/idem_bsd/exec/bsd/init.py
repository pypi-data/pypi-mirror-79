import os


def __sub_virtual__(hub):
    try:
        if os.uname().sysname.upper().endswith("BSD"):
            return True
    except:
        ...
    return False, "idem-bsd is only intended for BSD systems"
