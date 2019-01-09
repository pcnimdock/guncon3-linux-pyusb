# guncon3-linux-pyusb
Script de python para el manejo de la pistola de NAMCO Guncon3 para linux

Basado en el kernel driver aportado por https://github.com/beardypig/guncon3

El script usa las librerías
python-uinput
pyusb
libevdev

# Uso
Hay que dar permisos a la lectura de uinput con
sudo setfacl -m user:usuario:rw /dev/uinput
donde usuario es el nombre del usuario que vaya a manejar la pistola

Los permisos para habilitar la lectura por usb se deberá incluir el archivo 
/etc/udev/rules.d/99-guncon3.rules
con el siguiente contenido

 SUBSYSTEM=="usb", ATTR{idVendor}=="0b9a", ATTR{idProduct}=="0800", MODE="0666", GROUP="plugdev", TAG+="uaccess", TAG+="udev-acl", SYMLINK+="guncon3%n"
 KERNEL=="hidraw*", ATTRS{idVendor}=="0b9a", ATTRS{idProduct}=="0800",  MODE="0666", GROUP="plugdev", TAG+="uaccess", TAG+="udev-acl"
 
Para ejecutar el script

 python3 guncon3-linux-pyusb

El calibrado se puede realizar con el jstest-gtk

En ubuntu 18.04 no es posible calibrar la pistola sólamente con jstest-gtk, y no hay (o no he encontrado) un modo gráfico para esto. 
Para la calibración habrá que hacer una combinación con jstest-gtk y en el comando en terminal "evdev-joystick" de esta forma:

1.- Abrir jstest-gtk e ir al mando asociado a la pistola y dar a propiedades
2.- Luego a calibración
3.- Con la pistola apuntando al centro, apretar a empezar calibración
4.- Apuntar con la pistola los extremos o perímetro* de la pantalla (mantener la pistola siempre dentro del perímetro).
5.- Aceptar

Esto nos dará los rangos mínimo y máximo a aplicar con evdev-joystick
Antes hay que saber la ruta del mando para ello en modo terminal, escribimos
evemu-describe
Dará una salida tal que así

Available devices:
/dev/input/event11:	4-Axis,9-Button
Select the device event number [0-11]: 
Por tanto la ruta será /dev/input/event11

A partir de aquí se irá escribiendo los valores mínimos que ha dado jstest

sudo evdev-joystick --evdev /ruta --axis numero_de_eje -m valor_minimo -M valor_maximo
Por ejemplo, mi calibración es la siguiente:
sudo evdev-joystick --evdev /dev/input/event11 --axis 1 -m 2311 -M 30440
sudo evdev-joystick --evdev /dev/input/event11 --axis 2 -m 0 -M 255
sudo evdev-joystick --evdev /dev/input/event11 --axis 3 -m 0 -M 255
sudo evdev-joystick --evdev /dev/input/event11 --axis 4 -m 0 -M 255
sudo evdev-joystick --evdev /dev/input/event11 --axis 5 -m 0 -M 255

No he conseguido configurarlo con advancemame (documentación nula) pero sí que he podido hacerlo con gnome-video-arcade y la versión de mame de los repositorios de ubuntu.
Mame aplica una zona muerta al mando que se corrige de la siguiente forma en terminal
cd ~
cd ~/.mame
mame -cc
Con esto creamos el archivo de configuración mame.ini
Dentro del archivo hay una opción que es "joystick_deadzone" que por defecto está a 0.3. Aquí hay que colocar 0


*Para calibrar con gnome-video-arcade yo he capturado la pantalla en un juego y como perímetro he usado el contenido de la imagen


