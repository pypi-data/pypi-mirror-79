async def load_defaults(hub):
    # Hard-coded grains for mac
    hub.grains.GRAINS.init = "launchd"
    hub.grains.GRAINS.osmanufacturer = hub.grains.GRAINS.manufacturer = "Apple Inc."
    hub.grains.GRAINS.os_family = "MacOS"
    hub.grains.GRAINS.ps = "ps auxwww"
