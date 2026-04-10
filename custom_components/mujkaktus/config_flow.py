import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from pymujkaktus import KaktusAPI

from .const import DOMAIN, CONF_USERNAME, CONF_PASSWORD

class KaktusConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Můj Kaktus."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            try:
                # Validace přihlášení
                api = KaktusAPI(user_input[CONF_USERNAME], user_input[CONF_PASSWORD])
                # Pro validaci zkusíme login v executoru
                success = await self.hass.async_add_executor_job(api.login)
                if success:
                    return self.async_create_entry(title="Můj Kaktus", data=user_input)
                else:
                    errors["base"] = "invalid_auth"
            except Exception:
                errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_USERNAME): str,
                    vol.Required(CONF_PASSWORD): str,
                }
            ),
            errors=errors,
        )
