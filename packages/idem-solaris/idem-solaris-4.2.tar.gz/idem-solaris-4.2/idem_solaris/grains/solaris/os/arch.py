import os


async def load_arch(hub):
    (_, _, _, _, hub.grains.GRAINS.osarch,) = os.uname()
