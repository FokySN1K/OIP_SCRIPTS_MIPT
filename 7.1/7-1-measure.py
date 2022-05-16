import RPi.GPIO as gpio
import time
import matplotlib.pyplot as mplot


dac = [ 26, 19, 13, 6, 5, 11, 9, 10 ]
leds = [ 21, 20, 16, 12, 7, 8, 25, 24 ]
comp = 4
troyka = 17
Vref = 3.3
bdepth = 8 #хардкод разрядности
time_massiv = []

gpio.setmode( gpio.BCM )

gpio.setup( dac, gpio.OUT, initial=gpio.LOW )
gpio.setup( leds, gpio.OUT, initial=gpio.LOW )
gpio.setup( troyka, gpio.OUT, initial=gpio.HIGH )
gpio.setup( comp, gpio.IN )


def decimal2binary( value ):
    return [int(bit) for bit in bin( value ) [2:].zfill( bdepth )]

def adc():
    retvalue = 0
    decVtest = 0
    for testbit in reversed( range( bdepth ) ):
        decVtest = retvalue + 2 ** testbit
        gpio.output( dac, decimal2binary( decVtest ) )
        time.sleep( 0.001 )
        compsignal = gpio.input( comp )

        if compsignal == 1: 
            retvalue += 2 ** testbit

    return retvalue


try:
    data = []
    start_time = time.time()
    phase1_passed = False


    while True:
        decVfind = adc()
        binVfind = decimal2binary( decVfind )

        volume = round( decVfind / ( 2 ** bdepth ) * bdepth ) 
        gpio.output( leds[:volume], 1 )
        gpio.output( leds[volume:], 0 )

        print('decimal V = {}'.format( decVfind ))
        print('binary V = {}'.format( binVfind ))
        print('V = {}'.format( decVfind / ( 2 ** bdepth ) * Vref ))
        print( '' )


        data = data + [ decVfind ]
        time_massiv.append(time.time() - start_time)
        if decVfind >= 0.97 * ( 2 ** bdepth ):
            gpio.output( troyka, 0 )
            phase1_passed = True

        if phase1_passed == True | decVfind <= 0.02 * ( 2 ** bdepth ):
            break

    end_time = time.time()
    duration = end_time - start_time

    print('duration = {} s'.format( duration ))

    mplot.plot( time_massiv, data)

    data_str = "\n".join( [ str( item ) for item in data ] )
    with open( "data.txt", "w" ) as datafile:
        datafile.write( data_str )

    sample_rate = len( data ) / duration
    quantization = Vref / ( 2 ** bdepth )

    print('sample rate = {} Hz'.format( sample_rate ))
    print('quantization = {} V'.format( quantization ))

    with open( "settings.txt", "w" ) as settingsfile:
        settingsfile.write( 'samplerate={}\n'.format( sample_rate ) )
        settingsfile.write( 'quantization={}'.format( quantization ) )

    mplot.show()

finally:
    gpio.output( dac + leds + [troyka], 0 )
    gpio.cleanup()