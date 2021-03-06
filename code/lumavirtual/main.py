#!/usr/bin/env python3

from luma.core.device import device
from luma.core.render import canvas
from demo_opts import get_device
import luma.core.legacy.font
from luma.core.legacy.font import proportional
from luma.core.legacy import text, textsize
from time import sleep
from mohanfont import SEG7_CUSTOM_FONT

class wledluma(device):
    def __init__(self, dma_interface=None, width=20, height=7, cascaded=None,
                 rotate=0, mapping=None, **kwargs):
        #super(device, self).__init__()

        # Derive (override) the width and height if a cascaded param supplied
        if cascaded is not None:
            width = cascaded
            height = 1

        self.cascaded = width * height
        self.capabilities(width, height, rotate, mode="RGB")
        self._mapping = list(mapping or range(self.cascaded))
        assert(self.cascaded == len(self._mapping))
        self._contrast = 255
        self._prev_contrast = 255

        #ws = self._ws = dma_interface or self.__ws281x__()

        # Create ws2811_t structure and fill in parameters.
        #self._leds = ws.new_ws2811_t()

        #pin = 18
        #channel = 0
        #dma = 10
        #freq_hz = 800000
        #brightness = 255
        #strip_type = ws.WS2811_STRIP_GRB
        #invert = False

        # Initialize the channels to zero
        #for channum in range(2):
        #    chan = ws.ws2811_channel_get(self._leds, channum)
        #    ws.ws2811_channel_t_count_set(chan, 0)
        #    ws.ws2811_channel_t_gpionum_set(chan, 0)
        #    ws.ws2811_channel_t_invert_set(chan, 0)
        #    ws.ws2811_channel_t_brightness_set(chan, 0)

        # Initialize the channel in use
        #self._channel = ws.ws2811_channel_get(self._leds, channel)
        #ws.ws2811_channel_t_count_set(self._channel, self.cascaded)
        #ws.ws2811_channel_t_gpionum_set(self._channel, pin)
        #ws.ws2811_channel_t_invert_set(self._channel, 0 if not invert else 1)
        #ws.ws2811_channel_t_brightness_set(self._channel, brightness)
        #ws.ws2811_channel_t_strip_type_set(self._channel, strip_type)

        # Initialize the controller
        #ws.ws2811_t_freq_set(self._leds, freq_hz)
        #ws.ws2811_t_dmanum_set(self._leds, dma)

        #resp = ws.ws2811_init(self._leds)
        #if resp != 0:
        #    raise RuntimeError(f'ws2811_init failed with code {resp}')

        self.clear()
        self.show()

    def __ws281x__(self):
        pass
        #import _rpi_ws281x
        #return _rpi_ws281x

    def display(self, image):
        """
        Takes a 24-bit RGB :py:mod:`PIL.Image` and dumps it to the daisy-chained
        WS2812 neopixels.
        """
        assert(image.mode == self.mode)
        assert(image.size == self.size)

        #ws = self._ws
        m = self._mapping
        for idx, (red, green, blue) in enumerate(image.getdata()):
            #color = (red << 16) | (green << 8) | blue
            print(f"idx:{idx} red: {red} green: {green} blue: {blue} m: {m[idx]}")
            #ws.ws2811_led_set(self._channel, m[idx], color)

        self._flush()

    def show(self):
        """
        Simulates switching the display mode ON; this is achieved by restoring
        the contrast to the level prior to the last time hide() was called.
        """
        if self._prev_contrast is not None:
            self.contrast(self._prev_contrast)
            self._prev_contrast = None

    def hide(self):
        """
        Simulates switching the display mode OFF; this is achieved by setting
        the contrast level to zero.
        """
        if self._prev_contrast is None:
            self._prev_contrast = self._contrast
            self.contrast(0x00)

    def contrast(self, value):
        """
        Sets the LED intensity to the desired level, in the range 0-255.
        :param level: Desired contrast level in the range of 0-255.
        :type level: int
        """
        assert(0x00 <= value <= 0xFF)
        self._contrast = value
        #self._ws.ws2811_channel_t_brightness_set(self._channel, value)
        self._flush()

    def _flush(self):
        pass
        #resp = self._ws.ws2811_render(self._leds)
        #if resp != 0:
        #    raise RuntimeError('ws2811_render failed with code {0}'.format(resp))

    def __del__(self):
        pass
        # Required because Python will complain about memory leaks
        # However there's no guarantee that "ws" will even be set
        # when the __del__ method for this class is reached.
        #if self._ws is not None:
        #    self.cleanup()

    def cleanup(self):
        """
        Attempt to reset the device & switching it off prior to exiting the
        python process.
        """
        self.hide()
        self.clear()

        
        #if self._leds is not None:
            #self._ws.ws2811_fini(self._leds)
            #self._ws.delete_ws2811_t(self._leds)
        self._leds = None
        self._channel = None  
    



if __name__ == "__main__":
    d = get_device()
    
    #wled = wledluma()
    #with canvas(wled) as draw:
    font = getattr(luma.core.legacy.font, "SEG7_FONT")
    alphanum = list(filter(str.isalnum,map(chr,range(123))))
    n = 5
    lots_of_five_alphanums = [alphanum[i * n:(i + 1) * n] for i in range((len(alphanum) + n - 1) // n )] 
    lots_of_five_alphanums[-1].append(".")
    lots_of_five_alphanums[-1].append(".")
    lots_of_five_alphanums[-1].append(".")    
    #print(lots_of_five_alphanums)
   
    
    with canvas(d) as draw:
        #draw.point((0,0), fill="red")
        #draw.text((-1,-2), "_")
        font = SEG7_CUSTOM_FONT
        #text(draw, (0,-6), "ABCD", "red", font=proportional(font))
        text(draw, (3,-1), "ABCD", "red", font=proportional(font))
    sleep(30)
    

    '''
    for i,_ in enumerate(lots_of_five_alphanums):
        #print(i)
        with canvas(d) as draw:
            text(draw, (0, -1), "".join(lots_of_five_alphanums[i]), "red", font=proportional(font))
        sleep(10)
    '''

'''
    with canvas(d) as draw:
        #draw.point((0,0), fill="white")
        #draw.text((0,-3), "ABC" ,fill="white", font=font)
        text(draw, (0, -1), "abcde", "red", font=proportional(font))

    sleep(10)

    with canvas(d) as draw:
        #draw.point((0,0), fill="white")
        #draw.text((0,-3), "ABC" ,fill="white", font=font)
        text(draw, (0, -1), "fghij", "red", font=proportional(font))

    sleep (10)
'''