# jetson-orin-gpio-patch
Addressing GPIO issue in JetPack 6.2
# TESTING - EXPLORING - WIP

## Overall Purpose of the Patch
This patch improves the Tegra pinctrl driver’s handling of GPIO pin multiplexing by:
* Preserving Original Pin State: Previously, when a GPIO was requested, the sfsel bit was cleared (forcing GPIO mode), and when freed, it was always set (forcing special function mode). Now, the driver remembers the original state and restores it when the GPIO is freed.
* Adding Configuration Tracking: The pingroup_configs array introduces a mechanism to store per-group state, making the driver more flexible for future enhancements.
* Avoiding Unnecessary Changes: The conditional restoration of the sfsel bit prevents unnecessary register writes, improving efficiency and reducing side effects.

Pins are shared between GPIO and special functions (e.g., I2C, SPI), these changes ensure proper state management when switching between modes.

