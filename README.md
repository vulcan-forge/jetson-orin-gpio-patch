# jetson-orin-gpio-patch
Addressing GPIO issue in JetPack 6.2
# TESTING - EXPLORING - WIP

In the default JetPack 6.2 distribution, GPIO pins are not marked as bidirectional. In order to change that, here is an example device tree overlay file. This is for Pin 7, which is GPIO9/AUD_MCLK. This pin translates to Linux name soc_gpio59_pac6. In order to compile the .dts file, copy it to the /boot directory, and then use jetson-io.py to add it to the /boot/extlinux/extlinux.conf file:
```bash
dtc -O dtb -o pin7_as_gpio.dtbo pin7_as_gpio.dts 
sudo cp pin7_as_gpio.dtbo /boot
sudo /opt/nvidia/jetson-io/jetson-io.py
```

## Test examples
You will need to reboot for the changes to take effect. There are sample programs taken from the Jetson.GPIO library, which use Pin 7 as an output and Pin 15 as in input.

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
Use Python to launch the examples.

# Kernel Patch
Also included is the kernel patch which fixes an issue with how the sfsel bit is handled. There is a shell script to help build the kernel image. The script assumes that you are using the JetsonHacks jetson-orin-build-kernel tools.

## Overall Purpose of the Patch
This patch improves the Tegra pinctrl driver’s handling of GPIO pin multiplexing by:
* Preserving Original Pin State: Previously, when a GPIO was requested, the sfsel bit was cleared (forcing GPIO mode), and when freed, it was always set (forcing special function mode). Now, the driver remembers the original state and restores it when the GPIO is freed.
* Adding Configuration Tracking: The pingroup_configs array introduces a mechanism to store per-group state, making the driver more flexible for future enhancements.
* Avoiding Unnecessary Changes: The conditional restoration of the sfsel bit prevents unnecessary register writes, improving efficiency and reducing side effects.

Pins are shared between GPIO and special functions (e.g., I2C, SPI), these changes ensure proper state management when switching between modes.

