# -*- coding: utf-8 -*-

"""
app config
"""

from django.apps import AppConfig

from . import __version__


class AaDiscordPingFormatterConfig(AppConfig):
    """
    application config
    """

    name = "discordpingformatter"
    label = "discordpingformatter"
    verbose_name = "Fleet Ping Formatter v{}".format(__version__)
