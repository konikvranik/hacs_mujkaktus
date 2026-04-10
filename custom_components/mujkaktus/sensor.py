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

    sensors = [
        KaktusCreditSensor(coordinator),
        KaktusHistorySensor(coordinator, "Calls", "calls"),
        KaktusHistorySensor(coordinator, "SMS", "sms"),
        KaktusHistorySensor(coordinator, "Data", "data"),
        KaktusHistorySensor(coordinator, "MMS", "mms"),
        KaktusHistorySensor(coordinator, "Recharges", "recharges"),
        KaktusHistorySensor(coordinator, "Roaming", "roaming"),
        KaktusHistorySensor(coordinator, "Audiotex", "audiotex"),
        KaktusHistorySensor(coordinator, "Other", "other"),
        KaktusHistorySensor(coordinator, "All", "all"),
    ]

    async_add_entities(sensors)

class KaktusCreditSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Kaktus Credit sensor."""

    def __init__(self, coordinator):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_name = "Kaktus Credit"
        self._attr_unique_id = f"{coordinator.name}_credit"
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

    def __init__(self, coordinator, name, key):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._key = key
        self._attr_name = f"Kaktus {name} History"
        self._attr_unique_id = f"{coordinator.name}_{key}_history"
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
            return {
                "history": self.coordinator.data.get(self._key)
            }
        return {}
