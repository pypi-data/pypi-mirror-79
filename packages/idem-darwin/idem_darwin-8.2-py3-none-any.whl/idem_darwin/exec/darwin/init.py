import os


def __sub_virtual__(hub):
    try:
        if os.uname().sysname == "Darwin":
            return True
    except:
        ...

    return (
        False,
        "idem-darwin only runs on MacOS systems",
    )
