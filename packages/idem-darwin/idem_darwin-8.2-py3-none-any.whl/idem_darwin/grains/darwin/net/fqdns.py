import shutil


def __virtual__(hub):
    return shutil.which("scutil")


async def load_fqdns(hub):
    scutil = shutil.which("scutil")
    hub.grains.GRAINS.localhost = (
        await hub.exec.cmd.run([scutil, "--get", "LocalHostName"])
    ).stdout.strip()
    hostname = shutil.which("hostname")
    if hostname:
        hub.grains.GRAINS.fqdn = (
            await hub.exec.cmd.run([hostname, "-f"])
        ).stdout.strip()

        hub.log.debug("loading fqdns based grains")
        (
            hub.grains.GRAINS.host,
            hub.grains.GRAINS.domain,
        ) = hub.grains.GRAINS.fqdn.partition(".")[::2]
        if not hub.grains.GRAINS.domain:
            hub.grains.GRAINS.domain = "local"
            hub.grains.GRAINS.fqdn += ".local"
        if "." not in hub.grains.GRAINS.localhost:
            hub.grains.GRAINS.localhost += f".{hub.grains.GRAINS.domain}"
