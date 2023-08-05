import os

EXEC_PROFILE = os.environ.get("EXEC_PROFILE", "dev")

print(f"EXEC_PROFILE '{EXEC_PROFILE}' ", end="")

if EXEC_PROFILE == "dev":
    from .dev import *  # noqa
elif EXEC_PROFILE == "local":
    from .local import *  # noqa
else:
    # docker must be the default
    from .docker import *  # noqa
