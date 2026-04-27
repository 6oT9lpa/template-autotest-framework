class InfoMessages:
    DRIVER_CREATE = "Creating browser driver: browser={browser}, incognito={incognito}"
    DRIVER_READY = "Browser driver is ready"
    DRIVER_QUIT = "Browser driver was closed"
    OPEN_URL = "Opening URL: {url}"
    JS_CLICK = "Clicking element through JavaScript utility: element={element}"


class WarningMessages:
    STALE_ELEMENT_DURING_WAIT = "Stale element while waiting for locator={locator}"
    LOGGER_DISABLED = "Logging is disabled by configuration"


class ErrorMessages:
    UNSUPPORTED_BROWSER = "Unsupported browser requested: {browser}"
    WAIT_TIMEOUT = "Timeout while waiting for condition: timeout={timeout}"
    ELEMENT_NOT_VISIBLE = "Element was not visible: locator={locator}, timeout={timeout}"
    ELEMENT_NOT_CLICKABLE = "Element was not clickable: locator={locator}, timeout={timeout}"
