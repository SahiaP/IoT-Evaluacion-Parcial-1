import network, urequests, machine
from time import sleep

led = machine.Pin(13, machine.Pin.OUT)
LM35 = machine.ADC(0)
FactorConv = 3.3/65535
ssid = 'Alumno' 
password = 'Mebe2ege'

def ConnectWifi():
    red = network.WLAN(network.STA_IF)
    red.active(True)
    red.connect(ssid, password)
    while red.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = red.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip

ip = ConnectWifi()

server = "https://api.thingspeak.com/"
apikey = "IZGM57XWDP2BAVKZ"
field = 1

while True:
    try:
        LM35_V = LM35.read_u16()
        VoltConv = FactorConv*LM35_V
        Temperatura = VoltConv/(10.0/1000)
        led.on()
        print(f"T = {Temperatura}°C")
        url = f"{server}/update?apikey={apikey}&field{field}={Temperatura}"
        sleep(1)
        led.off()
        sleep(4)
        request = urequests.post(url)
        request.close()
    
    else Exception as e:
        print("ERROR: ", e)

