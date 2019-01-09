import sys
import usb.util
import libevdev
import time
from libevdev import InputEvent
from libevdev import InputAbsInfo
import ctypes

CONS_ABS1 = 0x0b
CONS_ABS2 = 0x0c

KEY_TABLE = bytes([
    0x75, 0xC3, 0x10, 0x31, 0xB5, 0xD3, 0x69, 0x84, 0x89, 0xBA, 0xD6, 0x89, 0xBD, 0x70, 0x19, 0x8E, 0x58, 0xA8,
    0x3D, 0x9B, 0x5D, 0xF0, 0x49, 0xE8, 0xAD, 0x9D, 0x7A, 0x0D, 0x7E, 0x24, 0xDA, 0xFC, 0x0D, 0x14, 0xC5, 0x23,
    0x91, 0x11, 0xF5, 0xC0, 0x4B, 0xCD, 0x44, 0x1C, 0xC5, 0x21, 0xDF, 0x61, 0x54, 0xED, 0xA2, 0x81, 0xB7, 0xE5,
    0x74, 0x94, 0xB0, 0x47, 0xEE, 0xF1, 0xA5, 0xBB, 0x21, 0xC8, 0x91, 0xFD, 0x4C, 0x8B, 0x20, 0xC1, 0x7C, 0x09, 0x58,
    0x14, 0xF6, 0x00, 0x52, 0x55, 0xBF, 0x41, 0x75, 0xC0, 0x13, 0x30, 0xB5, 0xD0, 0x69, 0x85, 0x89, 0xBB, 0xD6, 0x88,
    0xBC, 0x73, 0x18, 0x8D, 0x58, 0xAB, 0x3D, 0x98, 0x5C, 0xF2, 0x48, 0xE9, 0xAC, 0x9F, 0x7A, 0x0C, 0x7C, 0x25, 0xD8,
    0xFF, 0xDC, 0x7D, 0x08, 0xDB, 0xBC, 0x18, 0x8C, 0x1D, 0xD6, 0x3C, 0x35, 0xE1, 0x2C, 0x14, 0x8E, 0x64, 0x83, 0x39,
    0xB0, 0xE4, 0x4E, 0xF7, 0x51, 0x7B, 0xA8, 0x13, 0xAC, 0xE9, 0x43, 0xC0, 0x08, 0x25, 0x0E, 0x15, 0xC4, 0x20, 0x93,
    0x13, 0xF5, 0xC3, 0x48, 0xCC, 0x47, 0x1C, 0xC5, 0x20, 0xDE, 0x60, 0x55, 0xEE, 0xA0, 0x40, 0xB4, 0xE7, 0x74,
    0x95, 0xB0, 0x46, 0xEC, 0xF0, 0xA5, 0xB8, 0x23, 0xC8, 0x04, 0x06, 0xFC, 0x28, 0xCB, 0xF8, 0x17, 0x2C, 0x25, 0x1C,
    0xCB, 0x18, 0xE3, 0x6C, 0x80, 0x85, 0xDD, 0x7E, 0x09, 0xD9, 0xBC, 0x19, 0x8F, 0x1D, 0xD4, 0x3D, 0x37, 0xE1, 0x2F,
    0x15, 0x8D, 0x64, 0x06, 0x04, 0xFD, 0x29, 0xCF, 0xFA, 0x14, 0x2E, 0x25, 0x1F, 0xC9, 0x18, 0xE3, 0x6D, 0x81, 0x84,
    0x80, 0x3B, 0xB1, 0xE5, 0x4D, 0xF7, 0x51, 0x78, 0xA9, 0x13, 0xAD, 0xE9, 0x80, 0xC1, 0x0B, 0x25, 0x93, 0xFC,
    0x4D, 0x89, 0x23, 0xC2, 0x7C, 0x0B, 0x59, 0x15, 0xF6, 0x01, 0x50, 0x55, 0xBF, 0x81, 0x75, 0xC3, 0x10, 0x31, 0xB5,
    0xD3, 0x69, 0x84, 0x89, 0xBA, 0xD6, 0x89, 0xBD, 0x70, 0x19, 0x8E, 0x58, 0xA8, 0x3D, 0x9B, 0x5D, 0xF0, 0x49,
    0xE8, 0xAD, 0x9D, 0x7A, 0x0D, 0x7E, 0x24, 0xDA, 0xFC, 0x0D, 0x14, 0xC5, 0x23, 0x91, 0x11, 0xF5, 0xC0, 0x4B, 0xCD,
    0x44, 0x1C, 0xC5, 0x21, 0xDF, 0x61, 0x54, 0xED, 0xA2, 0x81, 0xB7, 0xE5, 0x74, 0x94, 0xB0, 0x47, 0xEE, 0xF1,
    0xA5, 0xBB, 0x21, 0xC8])

def open_dev():
    d = libevdev.Device()
    d.name = '4-Axis,9-Button'
    ai = InputAbsInfo(minimum=-32766, maximum=32767, resolution=1)
    ai2 = InputAbsInfo(minimum=-32767, maximum=32767, resolution=1)
    d.enable(libevdev.EV_ABS.ABS_X, ai)
    d.enable(libevdev.EV_ABS.ABS_Y, ai)
    d.enable(libevdev.EV_ABS.ABS_RX, ai2)
    d.enable(libevdev.EV_ABS.ABS_RY, ai2)
    d.enable(libevdev.EV_ABS.ABS_THROTTLE, ai2)
    d.enable(libevdev.EV_ABS.ABS_RUDDER, ai2)
    d.enable(libevdev.EV_KEY.BTN_TRIGGER)
    d.enable(libevdev.EV_KEY.BTN_0)
    d.enable(libevdev.EV_KEY.BTN_1)
    d.enable(libevdev.EV_KEY.BTN_2)
    d.enable(libevdev.EV_KEY.BTN_3)
    d.enable(libevdev.EV_KEY.BTN_4)
    d.enable(libevdev.EV_KEY.BTN_5)
    d.enable(libevdev.EV_KEY.BTN_6)
    d.enable(libevdev.EV_KEY.BTN_7)
    d.enable(libevdev.EV_KEY.BTN_8)
    uinput = d.create_uinput_device()
    return uinput

def open_mouse(x_min,x_max,y_min,y_max):
    d = libevdev.Device()
    d.name = 'Guncon3_Touch'
    ai = InputAbsInfo(minimum=x_min, maximum=x_max, resolution=1)
    ai2 = InputAbsInfo(minimum=y_min, maximum=y_max, resolution=1)
    ai3 = InputAbsInfo(minimum=0, maximum=255, resolution=1)
    d.enable(libevdev.EV_ABS.ABS_X, ai)
    d.enable(libevdev.EV_ABS.ABS_Y, ai2)
    d.enable(libevdec.EV_ABS.ABS_PRESSURE,ai3)
    d.enable(libevdev.EV_KEY.BTN_TOUCH)
    d.enable(libevdev.EV_KEY.BTN_RIGHT)
    d.enable(libevdev.EV_KEY.BTN_TOOL_FINGER)
    uinput = d.create_uinput_device()
    return uinput


abs_x_ant = int(0)
abs_y_ant = int(0)

def obtain_event(dec):
    "Obtener los eventos"
    #abs_x el punto medio es 0, el valor es signed, (-) izquierda del centro, (+) derecha del centro
    global abs_x_final
    global abs_y_final
    global btn_trigger_final
    global btn_0_final

    abs_x=dec[4] * 256 + dec[3]
    #abs_y el punto medio es 0, el valor es signed, (-) abajo del centro, (+) arriba del centro
    abs_y=dec[6] * 256 + data[5]
    #abs_z se acerca a rango de 0 a 0xffff, cuanto más cerca, el número más bajo
    #abs_z hace referencia a la distancia entre referencias en el campo de visión. Es la resta del campo de visión de la cámara menos la distancia entre referencias
    abs_z=dec[8] * 256 + dec[7]
    val_z = 65535-abs_z
    val_x = int(abs_x)
    val_y = int(abs_y)
    if val_x > 32767:
        abs_x= (-1)*(65535-val_x)
    #if val_y > 32767:
    #    abs_y= (1)*(65535-val_y)
    #abs_x = abs_x*2+3640
    #abs_y = (-1) * (abs_y*5+43043)
    number = abs_x & 0xFFFF
    abs_x = ctypes.c_int16(number).value
    number = abs_y & 0xFFFF
    abs_y = ctypes.c_int16(number).value
    #invertir ejes
    abs_y = (-1) * abs_y
    #print("abs_x:" + hex(dec[4]*256+dec[3]) + " abs_y:" + hex(dec[6]*256+dec[5]) + " abs_z:" + hex(dec[8]*256+dec[7]))
    #print("fuera de rango de referencia de la pantalla: " + str((0, 1)[dec[1] & 0x08>0]))
    #print("Sólo hay una referencia led: " + str((0, 1)[dec[1] & 0x10>0]))    
    abs_rx=dec[11]
    abs_ry=dec[12]
    abs_hat0x=dec[9]
    abs_hat0y=dec[10]
    btn_trigger= (0, 1)[dec[1] & 0x20>0]
    btn_0= (0, 1)[dec[0] & 0x04>0]
    btn_1= (0, 1)[dec[0] & 0x02>0]
    btn_2= (0, 1)[dec[1] & 0x04>0]
    btn_3= (0, 1)[dec[1] & 0x02>0]
    btn_4= (0, 1)[dec[1] & 0x80>0]
    btn_5= (0, 1)[dec[0] & 0x08>0]
    btn_6= (0, 1)[dec[2] & 0x80>0]
    btn_7= (0, 1)[dec[2] & 0x40>0]
    only_one_led_reference = (0, 1)[dec[1] & 0x10>0]
    out_of_reference_range = (0, 1)[dec[1] & 0x08>0]
    abs_x_final = abs_x
    abs_y_final = abs_y
    btn_trigger_final = btn_trigger
    btn_0_final = (0, 1)[dec[1] & 0x08>0]
    event = [libevdev.InputEvent(libevdev.EV_ABS.ABS_X, abs_x),
             libevdev.InputEvent(libevdev.EV_ABS.ABS_Y, abs_y),
             libevdev.InputEvent(libevdev.EV_ABS.ABS_RX, abs_rx),
             libevdev.InputEvent(libevdev.EV_ABS.ABS_RY, abs_ry),
             libevdev.InputEvent(libevdev.EV_ABS.ABS_THROTTLE, abs_hat0x),
             libevdev.InputEvent(libevdev.EV_ABS.ABS_RUDDER, abs_hat0y),
             libevdev.InputEvent(libevdev.EV_KEY.BTN_TRIGGER, btn_trigger),
             libevdev.InputEvent(libevdev.EV_KEY.BTN_0, btn_0),
             libevdev.InputEvent(libevdev.EV_KEY.BTN_1, btn_1),
             libevdev.InputEvent(libevdev.EV_KEY.BTN_2, btn_2),
             libevdev.InputEvent(libevdev.EV_KEY.BTN_3, btn_3),
             libevdev.InputEvent(libevdev.EV_KEY.BTN_4, btn_4),
             libevdev.InputEvent(libevdev.EV_KEY.BTN_5, btn_5),
             libevdev.InputEvent(libevdev.EV_KEY.BTN_6, btn_6),
             libevdev.InputEvent(libevdev.EV_KEY.BTN_7, btn_7),
             libevdev.InputEvent(libevdev.EV_KEY.BTN_8, btn_0_final),
             libevdev.InputEvent(libevdev.EV_SYN.SYN_REPORT, 0)]
    return event




def guncon3_decode(data, key):
    "Decodificar datos recibidos"
    data2 = bytearray(13)
    b_sum = data[13] ^ data[12]
    b_sum = b_sum + data[11] + data[10] - data[9] - data[8]
    b_sum = b_sum ^ data[7]
    b_sum = b_sum & 0xFF
    # b_sum = ((data[13] ^ data[12]) + data[11] + data[10] - data[9] - data[8]) ^ data[7]
    # a_sum = (((data[6]^b_sum)-data[5]-data[4])^data[3])+data[2]+data[1]-data[0]
    a_sum = data[6] ^ b_sum
    a_sum = a_sum - data[5] - data[4]
    a_sum = a_sum ^ data[3]
    a_sum = a_sum + data[2] + data[1] - data[0]
    a_sum = a_sum & 0xFF
    #print("a_sum")
    #print(a_sum)
    #print("key7")
    #print(hex(key[7]))
    #print("key")
    #print(key.hex())
    #print("data")
    #print(data.hex())
    if a_sum != key[7]:
        #print("Error checksum dec")
        return -1

    # key_offset = (((((key[1] ^ key[2]) - key[3] - key[4]) ^ key[5]) + key[6] - key[7]) ^ data[14]) + 0x26
    key_offset = key[1] ^ key[2]
    key_offset = key_offset - key[3] - key[4]
    key_offset = key_offset ^ key[5]
    key_offset = key_offset + key[6] - key[7]
    key_offset = key_offset ^ data[14]
    key_offset = key_offset + 0x26
    key_offset = key_offset & 0xFF
    key_index = 4
    # byte E is part of the key offset
    # byte D is ignored, possibly a padding byte - make the checksum workout

    for x in range(12, -1, -1):
        byte_x = data[x]
        for y in range(4, 1, -1):
            # loop 3 times
            key_offset = key_offset - 1
            bkey = KEY_TABLE[key_offset + 0x41]
            keyr = key[key_index]
            key_index = key_index - 1
            if key_index == 0:
                key_index = 7

            if (bkey & 3) == 0:
                byte_x = (byte_x - bkey) - keyr
            elif ((bkey & 3) == 1):
                byte_x = ((byte_x + bkey) + keyr)
            else:
                byte_x = ((byte_x ^ bkey) ^ keyr)
        byte_x = byte_x & 0xFF
        data2[x] = byte_x

    return data2


if __name__ == '__main__':
    # find our device
    dev = usb.core.find(idVendor=0x0b9a, idProduct=0x0800)
    x_min_cal = x_max_cal = y_min_cal = y_max_cal = 0
    # was it found?
    if dev is None:
        raise ValueError('Device not found')

    try:
        if dev.is_kernel_driver_active(0) is True:
            dev.detach_kernel_driver(0)
    except usb.core.USBError as e:
        sys.exit("El kernel no quiere dar el control del bicho")

    try:
        dev.set_configuration()
        dev.reset()
    except usb.core.USBError as e:
        sys.exit("No se puede configurar el bicho")

    # set the active configuration. With no arguments, the first
    # configuration will be the active one
    # dev.set_configuration()

    # get an endpoint instance
    # cfg = dev.get_active_configuration()
    cfg = dev[0]
    intf = cfg[(0, 0)]

    # ep = usb.util.find_descriptor(
    #        intf,
    #        # match the first OUT endpoint
    #        custom_match = \
    #        lambda e: \
    #            usb.util.endpoint_direction(e.bEndpointAddress) == \
    #            usb.util.ENDPOINT_OUT)

    epout = intf[0]
    epin = intf[1]

    assert epout is not None

    # write the data
    # ep.write('test')
    #print("print epout")
    #print(epout)
    #print("print ep2")
    #print(epin)
    #print("print cfg")
    #print(cfg)
    #print("print intf")
    #print(intf)

    # write data ep
    key = bytes([0x01, 0x12, 0x6F, 0x32, 0x24, 0x60, 0x17, 0x21])
    epout.write(key)
    data = dev.read(epin.bEndpointAddress, epin.wMaxPacketSize, timeout=100)
    uinput = open_dev()

    while 1:
        try:
            data = dev.read(epin.bEndpointAddress, epin.wMaxPacketSize, timeout=100)
            #print("data:")
            #print(data)
            #calibracion
            data_byte = bytearray()
            data_byte.append(data[0])
            data_byte.append(data[1])
            data_byte.append(data[2])
            data_byte.append(data[3])
            data_byte.append(data[4])
            data_byte.append(data[5])
            data_byte.append(data[6])
            data_byte.append(data[7])
            data_byte.append(data[8])
            data_byte.append(data[9])
            data_byte.append(data[10])
            data_byte.append(data[11])
            data_byte.append(data[12])
            data_byte.append(data[13])
            data_byte.append(data[14])
            dec = guncon3_decode(data_byte, key)
            #print(dec.hex())
            botones = obtain_event(dec)
            uinput.send_events(botones)
            print("X:" + str(abs_x_final))
            print("Y:" + str(abs_y_final))
            print("PUM!:" + str(btn_trigger_final))
            print("RECARGA:" + str(btn_0_final))
            

        except usb.core.USBError as e:
            if e.errno != 110:
                sys.exit("Error readin data: %s" % str(e))
