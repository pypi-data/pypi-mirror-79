import os


def __sub_virtual__(hub):
    try:
        if os.uname().sysname == "SunOS":
            return True
    except:
        ...
    return (
        False,
        "idem-solaris is only intended for SunOs systems",
    )
