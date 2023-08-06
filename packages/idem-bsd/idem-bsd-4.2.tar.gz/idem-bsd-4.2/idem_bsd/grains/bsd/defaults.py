async def load_defaults(hub):
    # Hard coded grains for BSD
    hub.grains.GRAINS.os_family = "BSD"
    hub.grains.GRAINS.ps = "ps auxwww"
