async def load_defaults(hub):
    # Hard coded grains for AIX systems
    hub.grains.GRAINS.os_family = hub.grains.GRAINS.os = "AIX"
    hub.grains.GRAINS.osmanufacturer = "International Business Machines Corporation"
    hub.grains.GRAINS.virtual = "physical"
    hub.grains.GRAINS.ps = "/usr/bin/ps auxww"
