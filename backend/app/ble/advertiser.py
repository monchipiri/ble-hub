class BleAdvertiserService:
    """Placeholder for BlueZ D-Bus BLE advertising implementation.

    The MVP exposes the service contract. Real advertising should register an
    LEAdvertisement1 object through org.bluez.LEAdvertisingManager1 on hci1.
    """

    def __init__(self) -> None:
        self.running = False
        self.payload: dict = {}

    async def start(self, payload: dict | None = None) -> None:
        self.payload = payload or {}
        self.running = True

    async def stop(self) -> None:
        self.running = False

    async def status(self) -> dict:
        return {"running": self.running, "payload": self.payload}
