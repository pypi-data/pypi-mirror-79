from django.conf import settings

from .utils import clean_setting

import re

# set default panels if none are set in local.py
AA_FLEETPINGFORMATTER_USE_SLACK = clean_setting(
    "AA_FLEETPINGFORMATTER_USE_SLACK", False
)


def get_site_url():  # regex sso url
    """
    get the site url
    :return: string
    """
    regex = r"^(.+)\/s.+"
    matches = re.finditer(regex, settings.ESI_SSO_CALLBACK_URL, re.MULTILINE)
    url = "http://"

    for m in matches:
        url = m.groups()[0]  # first match

    return url


def timezones_installed():
    return "timezones" in settings.INSTALLED_APPS
