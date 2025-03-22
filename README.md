# jetson-orin-gpio-patch
Addressing GPIO issue in JetPack 6.2
# TESTING - EXPLORING - WIP

## Test Example
The example test script should product 3.3V on pin 7. To install the Jetson.GPIO library:
```bash
sudo apt update
sudo apt install python3 python3-pip -y
sudo pip3 install Jetson.GPIO
```
You can use sudo when calling the scripts, or put the user in the gpio group:
```bash
sudo usermod -a -G gpio $USER
```
Reboot or logout/login to make the changes take effect.
```bash
sudo reboot
```
You can test to make sure the Jetson.GPIO library loads:
```bash
python3 -c "import Jetson.GPIO; print(Jetson.GPIO.__version__)"
```
You are then ready to run the example:
```bash
python example.py
```


## Overall Purpose of the Patch
This patch improves the Tegra pinctrl driver’s handling of GPIO pin multiplexing by:
* Preserving Original Pin State: Previously, when a GPIO was requested, the sfsel bit was cleared (forcing GPIO mode), and when freed, it was always set (forcing special function mode). Now, the driver remembers the original state and restores it when the GPIO is freed.
* Adding Configuration Tracking: The pingroup_configs array introduces a mechanism to store per-group state, making the driver more flexible for future enhancements.
* Avoiding Unnecessary Changes: The conditional restoration of the sfsel bit prevents unnecessary register writes, improving efficiency and reducing side effects.

Pins are shared between GPIO and special functions (e.g., I2C, SPI), these changes ensure proper state management when switching between modes.

