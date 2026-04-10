from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Můj Kaktus sensors."""
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]

    sensors = [
        KaktusCreditSensor(entry, coordinator),
        KaktusHistorySensor(entry, coordinator, "Calls", "calls"),
        KaktusHistorySensor(entry, coordinator, "SMS", "sms"),
        KaktusHistorySensor(entry, coordinator, "Data", "data"),
        KaktusHistorySensor(entry, coordinator, "MMS", "mms"),
        KaktusHistorySensor(entry, coordinator, "Recharges", "recharges"),
        KaktusHistorySensor(entry, coordinator, "Roaming", "roaming"),
        KaktusHistorySensor(entry, coordinator, "Audiotex", "audiotex"),
        KaktusHistorySensor(entry, coordinator, "Other", "other"),
        KaktusHistorySensor(entry, coordinator, "All", "all"),
    ]

    async_add_entities(sensors)


class KaktusCreditSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Kaktus Credit sensor."""

    def __init__(self, entry, coordinator):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_name = "Kaktus Credit"
        self._attr_unique_id = f"{entry.entry_id}_credit"
        self._attr_native_unit_of_measurement = "Kč"
        self._attr_icon = "mdi:cash-multiple"
        self._attr_device_info = DeviceInfo(
            entry_type=DeviceEntryType.SERVICE,
            identifiers={(DOMAIN, entry.entry_id)},
            name=f"Můj Kaktus ({entry.data.get('username', '')})",
            manufacturer="Můj Kaktus",
            configuration_url="https://mujkaktus.cz",
        )

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if self.coordinator.data:
            return self.coordinator.data.get("credit")
        return None


class KaktusHistorySensor(CoordinatorEntity, SensorEntity):
    """Representation of a Kaktus History sensor."""

    def __init__(self, entry, coordinator, name, key):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._key = key
        self._attr_name = f"Kaktus {name} History"
        self._attr_unique_id = f"{entry.entry_id}_{key}_history"
        self._attr_icon = "mdi:history"
        self._attr_device_info = DeviceInfo(
            entry_type=DeviceEntryType.SERVICE,
            identifiers={(DOMAIN, entry.entry_id)},
            name=f"Můj Kaktus ({entry.data.get('username', '')})",
            manufacturer="Můj Kaktus",
            configuration_url="https://mujkaktus.cz",
        )

    @property
    def native_value(self):
        """Return the state of the sensor (number of records)."""
        if self.coordinator.data:
            history = self.coordinator.data.get(self._key)
            if history:
                return len(history)
        return 0

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        if self.coordinator.data:
            return {"history": self.coordinator.data.get(self._key)}
        return {}
