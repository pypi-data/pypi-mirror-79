from discordpingformatter.models import (
    FleetComm,
    DiscordPingTargets,
    FleetType,
    Webhook,
    FleetDoctrine,
    FormupLocation,
)

from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required

from . import __title__

from .app_settings import (
    AA_FLEETPINGFORMATTER_USE_SLACK,
    get_site_url,
    timezones_installed,
)


@login_required
@permission_required("discordpingformatter.basic_access")
def index(request):
    """
    Index view
    """
    fleet_comms = FleetComm.objects.filter(is_enabled=True).order_by("name")

    discord_ping_targets = {}
    if AA_FLEETPINGFORMATTER_USE_SLACK is False:
        discord_ping_targets = (
            DiscordPingTargets.objects.filter(
                restricted_to_group__in=request.user.groups.all(), is_enabled=True
            )
            .distinct()
            .order_by("name")
        )

    fleet_types = FleetType.objects.filter(is_enabled=True).order_by("name")

    if AA_FLEETPINGFORMATTER_USE_SLACK is True:
        webhooks = (
            Webhook.objects.filter(
                type="Slack",
                restricted_to_group__in=request.user.groups.all(),
                is_enabled=True,
            )
            .distinct()
            .order_by("name")
        )
    else:
        webhooks = (
            Webhook.objects.filter(
                type="Discord",
                restricted_to_group__in=request.user.groups.all(),
                is_enabled=True,
            )
            .distinct()
            .order_by("name")
        )

    doctrines = FleetDoctrine.objects.filter(is_enabled=True).order_by("name")
    formup_locations = FormupLocation.objects.filter(is_enabled=True).order_by("name")

    context = {
        "title": __title__,
        "additionalPingTargets": discord_ping_targets,
        "additionalFleetTypes": fleet_types,
        "additionalPingWebhooks": webhooks,
        "fleetComms": fleet_comms,
        "fleetDoctrines": doctrines,
        "fleetFormupLocations": formup_locations,
        "site_url": get_site_url(),
        "timezones_installed": timezones_installed(),
        "mainCharacter": request.user.profile.main_character,
        "useSlack": AA_FLEETPINGFORMATTER_USE_SLACK,
    }

    return render(request, "discordpingformatter/index.html", context)
