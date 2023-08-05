import os

EXEC_PROFILE = os.environ.get("EXEC_PROFILE", "dev")
if EXEC_PROFILE == "local":
    from wedge.settings.local import *  # noqa
elif EXEC_PROFILE == "dev":
    from wedge.settings.dev import *  # noqa
elif EXEC_PROFILE == "ci":
    from wedge.settings.docker import *  # noqa
else:
    raise RuntimeError(f"You cannot run tests in '{EXEC_PROFILE}' environment")

# add email templates
TEMPLATES[0]["DIRS"].append(
    os.path.join(ROOT_DIR, "wedge/tests/fixtures/datasets/templates")
)

LOGGING = None
BASE_URL = "http://formatch.pytest.com"
INBOUND_CONTACT_TO = "pytest@mail.com"

# Email SMTP settings
DEFAULT_FROM_EMAIL = "from@test.fr"
DEFAULT_REPLY_TO = "noreply@test.fr"

# YouSign Url (without ending '/') and API key
YOUSIGN_API_URL = "https://staging-api.yousign.com"
YOUSIGN_API_KEY = "330fdd14a571dd22241ad8002f2ab545"
