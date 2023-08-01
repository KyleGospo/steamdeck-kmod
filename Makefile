obj-m += steamdeck.o
obj-m += extcon-steamdeck.o
obj-m += steamdeck-hwmon.o
obj-m += leds-steamdeck.o
obj-m += dwc3-pci.o

ccflags-y := -std=gnu99 -Wno-declaration-after-statement
KERNEL_SOURCE_DIR := /lib/modules/$(shell uname -r)/build

all:
	make -C "$(KERNEL_SOURCE_DIR)" M="$(PWD)" modules

clean:
	make -C "$(KERNEL_SOURCE_DIR)" M="$(PWD)" clean
