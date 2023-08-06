import sys


async def load_defaults(hub):
    # Determine if host is SmartOS (Illumos) or not
    hub.grains.GRAINS.smartos = sys.platform.startswith(
        "sunos"
    ) and hub.grains.GRAINS.kernelversion.startswith("joyent_")

    # Hard coded grains for SunOs go here:
