import os

def ensure_dir(f):
    """Ensure that a needed directory exists, creating it if it doesn't"""
    # print("Ensure dir")
    try:
        d = os.path.dirname(f)
        # print(d)

        if not os.path.exists(d):
            os.makedirs(d)

        return os.path.exists(f)
    except OSError:
        if not os.path.isdir(f):
            raise
    return None

