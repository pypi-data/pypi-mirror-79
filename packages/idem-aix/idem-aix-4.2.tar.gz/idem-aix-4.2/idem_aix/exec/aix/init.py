import os


def __sub_virtual__(hub):
    try:
        if os.uname().sysname == "AIX":
            return True
    except Exception:
        ...
    return False, "idem-aix only runs on AIX systems"
