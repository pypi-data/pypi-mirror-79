async def load_ps(hub):
    """
    Let anyone else try to set this grain first, then fallback to a default
    """
    if not await hub.grains.init.wait_for("ps"):
        hub.log.info("Using default Linux 'ps' grain")
        hub.grains.GRAINS.ps = "ps -efHww"
