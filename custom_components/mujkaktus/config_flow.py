import voluptuous as vol
from homeassistant import config_entries
from pymujkaktus import KaktusAPI, KaktusAuthError, KaktusConnectionError

from .const import DOMAIN, CONF_USERNAME, CONF_PASSWORD


class KaktusConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Můj Kaktus."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            try:
                api = KaktusAPI(user_input[CONF_USERNAME], user_input[CONF_PASSWORD])
                await self.hass.async_add_executor_job(api.login)

                await self.async_set_unique_id(user_input[CONF_USERNAME])
                self._abort_if_already_configured()

                return self.async_create_entry(
                    title=f"Můj Kaktus ({user_input[CONF_USERNAME]})",
                    data=user_input,
                )
            except KaktusAuthError:
                errors["base"] = "invalid_auth"
            except KaktusConnectionError:
                errors["base"] = "cannot_connect"
            except Exception:
                errors["base"] = "unknown"

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
