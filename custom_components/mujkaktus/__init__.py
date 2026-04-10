import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from pymujkaktus import KaktusAPI

from .const import DOMAIN, CONF_USERNAME, CONF_PASSWORD

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Můj Kaktus from a config entry."""
    username = entry.data[CONF_USERNAME]
    password = entry.data[CONF_PASSWORD]

    api = KaktusAPI(username, password)

    async def async_update_data():
        """Fetch data from API."""
        try:
            # V tuto chvíli je api synchronní, budeme ho volat v executoru
            return await hass.async_add_executor_job(update_api_data, api)
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="mujkaktus",
        update_method=async_update_data,
        update_interval=timedelta(hours=1),
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "api": api,
        "coordinator": coordinator,
    }

    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])

    return True

def update_api_data(api: KaktusAPI):
    """Synchronous data update."""
    if not api.logged_in:
        if not api.login():
            raise Exception("Login failed")
    
    return {
        "credit": api.get_credit(),
        "calls": api.get_call_history(),
        "sms": api.get_sms_history(),
        "data": api.get_data_history(),
        "mms": api.get_mms_history(),
        "recharges": api.get_recharge_history(),
        "roaming": api.get_roaming_history(),
        "audiotex": api.get_audiotex_history(),
        "other": api.get_other_history(),
        "all": api.get_all_history(),
    }

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["sensor"])
    if unload_ok:
        api = hass.data[DOMAIN][entry.entry_id]["api"]
        await hass.async_add_executor_job(api.close)
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
