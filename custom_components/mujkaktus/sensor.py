from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
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
    entry_id = entry.entry_id

    sensors = [
        KaktusCreditSensor(entry_id, coordinator),
        KaktusHistorySensor(entry_id, coordinator, "Calls", "calls"),
        KaktusHistorySensor(entry_id, coordinator, "SMS", "sms"),
        KaktusHistorySensor(entry_id, coordinator, "Data", "data"),
        KaktusHistorySensor(entry_id, coordinator, "MMS", "mms"),
        KaktusHistorySensor(entry_id, coordinator, "Recharges", "recharges"),
        KaktusHistorySensor(entry_id, coordinator, "Roaming", "roaming"),
        KaktusHistorySensor(entry_id, coordinator, "Audiotex", "audiotex"),
        KaktusHistorySensor(entry_id, coordinator, "Other", "other"),
        KaktusHistorySensor(entry_id, coordinator, "All", "all"),
    ]

    async_add_entities(sensors)


class KaktusCreditSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Kaktus Credit sensor."""

    def __init__(self, entry_id, coordinator):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_name = "Kaktus Credit"
        self._attr_unique_id = f"{entry_id}_credit"
        self._attr_native_unit_of_measurement = "Kč"
        self._attr_icon = "mdi:cash-multiple"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if self.coordinator.data:
            return self.coordinator.data.get("credit")
        return None


class KaktusHistorySensor(CoordinatorEntity, SensorEntity):
    """Representation of a Kaktus History sensor."""

    def __init__(self, entry_id, coordinator, name, key):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._key = key
        self._attr_name = f"Kaktus {name} History"
        self._attr_unique_id = f"{entry_id}_{key}_history"
        self._attr_icon = "mdi:history"

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
