Title: Arduino Hello World without IDE
Date: 2016-08-08
Tags: Arduino

There is already a number of resources available about programming the
Arduino with or without the IDE (I won't discuss here the pros and
cons of using it). This aims at being a quick memo for those who
already have some knowledge about C programming, and just want the
minimal information required to compile C code and upload it to an
Arduino board. This is basically a compilation of chunks of code
retrieved here and there a couple of months ago and possibly updated.

Packages to install
-------------------

To be able to compile and upload C code to an Arduino board, one has
to install the following packages:

* `avr-gcc` : Cross Compiling GNU GCC targeted at avr
* `avr-libc` : C library for use with GCC on Atmel AVR microcontrollers
* `avrdude` : Software for programming Atmel AVR microcontroller

Note the `avr-libc` (and to some extend `avr-gcc`) install a lot of
interesting libraries. Corresponding headers can be found in the
following directory: `/usr/avr/include/`.

Makefile
--------

The following Makefile summarizes the commands (with parameters)
needed to compile a C project and upload it to an Arduino board:

```makefile
baud=115200
avrType=atmega328p
avrFreq=16000000 # 16 Mhz
programmerDev=/dev/ttyUSB0
programmerType=arduino

cflags=-DF_CPU=$(avrFreq) -mmcu=$(avrType) -Wall -Werror -Wextra -Os
objects=$(patsubst %.c,%.o,$(wildcard *.c))

.PHONY: flash clean

all: main.hex

%.o: %.c
	avr-gcc $(cflags) -c $< -o $@

main.elf: $(objects)
	avr-gcc $(cflags) -o $@ $^

main.hex: main.elf
	avr-objcopy -j .text -j .data -O ihex $^ $@

flash: main.hex
	avrdude -p$(avrType) -c$(programmerType) -P$(programmerDev) -b$(baud) -v -U flash:w:$<

clean:
	rm -f main.hex main.elf $(objects)
```

To compile and upload a C project, one has to type the following
commands (actually the last one is enough, since it will automatically
build the `main.hex` file if required):

```bash
  $ make
  ...
  $ make flash
  ...
```

Depending on the board being used, one may have to tune the parameters
at the beginning of the file. For instance, the `avrType` must reflect
the type of AVR microcontroller on the board. The following header
contains an extensive list of the supported hardware:
`/usr/avr/include/avr/io.h`

Arduino Hello World
-------------------

The minimal program on an Arduino consists in having a LED blink. I
found this code somewhere (though I couldn't recover where from..):

```c
#include <util/delay.h>
#include <avr/io.h>

#define LED PORTB5

int main(void) {
  DDRB |= (1 << LED);
  for/*ever*/(;;) {
    PORTB |= (1 << LED);
    _delay_ms(100);
    PORTB &= (0 << LED);
    _delay_ms(100);
  }
}
```

That's all folks. With the packages installed and the Makefile
described earlier, one can compile this little C code and upload it to
an Arduino board and see the little red LED blinking. From this
starting point, one can easily work on bigger Arduino based projects.