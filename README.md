# guncon3-linux-pyusb
Script de python para el manejo de la pistola de NAMCO Guncon3 para linux

Basado en el kernel driver aportado por https://github.com/beardypig/guncon3

El script usa las librerías
python-uinput
pyusb
libevdev

Uso
Hay que dar permisos a la lectura de uinput con
sudo setfacl -m user:usuario:rw /dev/uinput
donde usuario es el nombre del usuario que vaya a manejar la pistola

Los permisos para habilitar la lectura por usb se deberá incluir el archivo /etc/udev/rules.d/99-guncon3.rules
con el siguiente contenido

SUBSYSTEM=="usb", ATTR{idVendor}=="0b9a", ATTR{idProduct}=="0800", MODE="0666", GROUP="plugdev", TAG+="uaccess", TAG+="udev-acl", SYMLINK+="guncon3%n"
KERNEL=="hidraw*", ATTRS{idVendor}=="0b9a", ATTRS{idProduct}=="0800",  MODE="0666", GROUP="plugdev", TAG+="uaccess", TAG+="udev-acl"
Para ejecutar el script
python3 guncon3-linux-pyusb

TODO
El calibrado ahora mismo es manual, cambiando los valores en el script abs_x y abs_y
Solo se ha probado su funcionamiento con sdl-jstest (https://github.com/meleu/jstest-sdl)
