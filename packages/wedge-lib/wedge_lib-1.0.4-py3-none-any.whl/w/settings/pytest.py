import os

EXEC_PROFILE = os.environ.get("EXEC_PROFILE", "dev")
if EXEC_PROFILE == "local":
    from w.settings.local import *  # noqa
elif EXEC_PROFILE == "dev":
    from w.settings.dev import *  # noqa
elif EXEC_PROFILE == "ci":
    from w.settings.docker import *  # noqa
else:
    raise RuntimeError(f"You cannot run tests in '{EXEC_PROFILE}' environment")

# add email templates
TEMPLATES[0]["DIRS"].append(
    os.path.join(ROOT_DIR, "w/tests/fixtures/datasets/templates")
)

LOGGING = None
BASE_URL = "http://formatch.pytest.com"
INBOUND_CONTACT_TO = "pytest@mail.com"

GOOGLE_MAP_SECRET = "AIzaSyAYU9lXqmmetI3s7feQi_Yc6_f7KGvVPz4"

MOCK_GMAP_CALLS = True
# Email SMTP settings
DEFAULT_FROM_EMAIL = "from@test.fr"
DEFAULT_REPLY_TO = "noreply@test.fr"

# YouSign Url (without ending '/') and API key
YOUSIGN_API_URL = "https://staging-api.yousign.com"
YOUSIGN_API_KEY = "330fdd14a571dd22241ad8002f2ab545"

RECAPTCHA_SECRET_KEY = "6Lfhir0ZAAAAAI7DnVanhzJFReZhoYi9_nRCiBvX"
