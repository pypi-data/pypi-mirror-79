from discordpingformatter.models import (
    FleetComm,
    Webhook,
    FleetDoctrine,
    FormupLocation,
    DiscordPingTargets,
    FleetType,
)

from django.contrib import admin


@admin.register(FleetComm)
class FleetCommAdmin(admin.ModelAdmin):
    list_display = ("name", "notes", "is_enabled")
    list_filter = ("is_enabled",)
    ordering = ("name",)


@admin.register(FleetDoctrine)
class FleetDoctrineAdmin(admin.ModelAdmin):
    list_display = ("name", "notes", "is_enabled")
    list_filter = ("is_enabled",)
    ordering = ("name",)


@admin.register(FormupLocation)
class FormupLocationAdmin(admin.ModelAdmin):
    list_display = ("name", "notes", "is_enabled")
    list_filter = ("is_enabled",)
    ordering = ("name",)


@admin.register(DiscordPingTargets)
class DiscordPingTargetsAdmin(admin.ModelAdmin):
    list_display = ("name", "discord_id", "notes", "is_enabled")
    list_filter = ("is_enabled",)
    ordering = ("name",)
    filter_horizontal = ("restricted_to_group",)


@admin.register(FleetType)
class FleetTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "embed_color", "notes", "is_enabled")
    list_filter = ("is_enabled",)
    ordering = ("name",)


@admin.register(Webhook)
class WebhookAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "type",
        "url",
        "notes",
        "is_embedded",
        "is_enabled",
    )
    list_filter = ("is_enabled",)
    ordering = ("name",)
    filter_horizontal = ("restricted_to_group",)
