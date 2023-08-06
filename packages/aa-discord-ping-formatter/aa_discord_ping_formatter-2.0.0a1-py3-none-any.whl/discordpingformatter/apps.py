from django.apps import AppConfig

from . import __version__


class AaDiscordPingFormatterConfig(AppConfig):
    name = "discordpingformatter"
    label = "discordpingformatter"
    verbose_name = "AA Fleet Ping Formatter v{}".format(__version__)
