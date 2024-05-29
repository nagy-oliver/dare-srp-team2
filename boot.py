import board
import storage
import digitalio
import external

# Remame drive to 'SRP-DARE-FC' 
storage.remount('/', readonly=False)

switch = external._ext_led
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP


m = storage.getmount('/')
m.label = 'SRP-DARE-FC'

storage.remount('/', readonly=not switch.value)

storage.enable_usb_drive()
