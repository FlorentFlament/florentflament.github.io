Title: Streaming music to YM2149F
Date: 2016-09-10
Tags: Arduino, YM2149, YM2149F, AY-3-8910

To follow-up on my previous blog post about [driving a YM2149F chip
with an Arduino][1], I wrote an Arduino firmware that can be used
together with a PC side Python script to send music to the
YM2149F. All the code is available in the [ym2149-streamer
repository][2] on GitHub.

Arduino Firmware
----------------

The first piece of code is the firmware. This is the code that runs in
the Arduino and drives the YM2149 chip. Most of the code is in the
`ym2149` library, which exports functions such as `send_data(char
addr, char data)` to write in the YM2149 registers, while complying
with the signals timings specified in the [YM2149 datasheet][3].

Basically, the firmware continuously reads the Arduino serial
line. Each time it has received 16 bytes, the firmware uses them to
set the 16 YM2149 registers (To be more precise only the first 14
registers are used, the 2 last registers are useless to play music).

Note that this code is specific to the circuit, and depends on how the
Arduino is wired to the YM2149. It has been written for (and tested
with) the circuit described in the blog post about [driving the YM2149
from an Arduino][1]

To flash the Arduino with the firmware:

* clone the [ym2149-streamer repository][2]
* and launch `make flash`

A couple of libraries need to be installed in order for the firmware
to compile and be uploaded to the Arduino. To setup your environment,
one can follow the instruction of the [Arduino Hello World without
IDE][6] blog post.


Playing music from a computer
-----------------------------

What remains to be done, is sending to the Arduino, the values of the
registers to be set in the YM2149. Here we can build on the [YM file
format created by Arnaud Carré][4]. The file format is quite straight
forward. It contains a header providing all the required information
about the tune, then a snapshot of the YM2149's 16 registers at
regular intervals (usually 50 times per second). To play the tune, we
have to send back the content of the YM2149 registers (sometimes
referred as the samples) at the appropriate frequency.

I wrote a small Python script, available in the [ym2149-streamer
repository][2], that parses a YM file and sends it to the Arduino
board. The syntax is:

    $ python streamer.py <output_device> <ym_filepath>

Note that `streamer.py` may work with other circuits driving a
YM2149. The only thing required is that the circuit be able to receive
a stream of YM2149's registers snapshots and send it to the chip each
time it receives a sample.

To illustrate this work, I published a video of the [YM2149F playing
Lemmings][5].

A [large YM tunes archive][7] allows playing old school musics on the
YM2149 chip. Note that the files in the zip archives are compressed
with `lha` (which can be installed through the Fedora `lha`
package). Therefore, one has to uncompress the `ym` files before
playing them with `streamer.py`. I may try to handle the decompression
directly in the script some day.

Besides, another [large archive of Atari ST music][8] is around there,
with a more dynamic community. Though the tunes are in the `sndh`
format, which is harder to interpret and stream to a YM2149 chip. A
nice thing would be to find a way to have these `sndh` files played on
the sound chip!


[1]: http://www.florentflament.com/blog/driving-ym2149f-sound-chip-with-an-arduino.html
[2]: https://github.com/FlorentFlament/ym2149-streamer
[3]: http://www.ym2149.com/ym2149.pdf
[4]: http://leonard.oxg.free.fr/ymformat.html
[5]: https://www.youtube.com/watch?v=MTRJdDbY048
[6]: http://www.florentflament.com/blog/arduino-hello-world-without-ide.html
[7]: http://pacidemo.planet-d.net/html.html
[8]: http://sndh.atari.org/