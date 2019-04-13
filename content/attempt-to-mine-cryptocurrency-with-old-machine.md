Title: Attempting to mine Cryptocurrency with an old machine
Date: 2019-04-13
Tags: AMD, Radeon, RX 480, GPU, Old Hardware, Cryptocurrency, GF7050T-M5

This is the story of me attempting to convert an old machine into a
Cryptocurrency miner. I basically tried to plug my AMD Radeon RX 480
graphic card into an old PC, a Core 2 duo with 4GB RAM and a
GF7050T-M5 motherboard.

* According to the [GF7050T-M5 manual][1], its PCI Express bus is most
  probably a PCI Express 1.0 x16 bus.

* While the [AMD Radeon RX 480][3] has a PCI Express 3.0 x16
  interface.

[Wikipedia's PCI Express pages][4] is not very clear regarding the
compatibility between PCI Express 3.0 and 1.0. At the very least, the
PCI Express 3.0 card fits into the PCI Express 1.0 slot. In the end, I
couldn't have the card working properly on the machine, though I did a
number of interesting findings.


## Booting on USB key

I made several OS installations (Ubuntu) on the machine using a
rewritable DVD-RW, because I failed to boot on a USB key. After
spending a bunch of time exploring the BIOS menu, I figured out that
the board allowed booting on USB keys with the following settings (in
the correct order):

* USB Legacy enabled
* Reboot, to have the USB key recognized by the BIOS
* First hard drive set to the USB key
* First boot device set to the USB key

This allowed much faster iterations, especially because I had to
remove the Radeon card to plug the DVD reader (The connector is placed
below the card, once plugged).


## Working text mode

Ubuntu 18.04 desktop, 18.04 server and 16.04 desktop installs load the
`amdgpu` driver at some point during boot time. When the Radeon RX 480
is plugged in the machine, the screen turns black at this moment. This
looks like the machine is completely crashed, but only the display is
actually missing. I can still connect to the machine through SSH
(having setup an SSH server before plugging the Radeon card).

Ubuntu 16.04 server never loads the `amdgpu` driver by default,
neither during the installation process, nor when booting on the
installed OS. I could install Ubuntu 16.04 server from a USB key and
run it properly, while the AMD Radeon card was plugged into the
machine.


## Driver crash

Both `amdgpu` and `amdgpu-pro` drivers crashed when loaded, whatever
the OS version I used:

* Ubuntu 16.04.3
* Ubuntu 16.04.5
* Ubuntu 18.04.2

The following trace is a typical one obtained from `dmesg` when
loading the `amdgpu` module. This one was obtained after having
installed the `amdgpu-pro-17.40` driver on Ubuntu 16.04.3:


```text
$ dmesg | grep "\[drm"
[    1.266917] [drm] Initialized drm 1.1.0 20060810
[    1.420705] [drm] amdgpu kernel modesetting enabled.
[    1.450320] [drm] initializing kernel modesetting (POLARIS10 0x1002:0x67DF 0x1002:0x0B37 0xC7).
[    1.450338] [drm] register mmio base: 0xFEBC0000
[    1.450342] [drm] register mmio size: 262144
[    1.450353] [drm] probing gen 2 caps for device 10de:56e = 113d01/0
[    1.450358] [drm] probing mlw for device 10de:56e = 113d01
[    1.450372] [drm] UVD is enabled in VM mode
[    1.450376] [drm] VCE enabled in VM mode
[    1.451068] [drm] GPU post is not needed
[    1.451090] [drm] vm size is 32 GB, block size is 13-bit, fragment size is 4-bit
[    1.451169] [drm] Detected VRAM RAM=8192M, BAR=256M
[    1.451173] [drm] RAM width 256bits GDDR5
[    1.451281] [drm] amdgpu: 8192M of VRAM memory ready
[    1.451286] [drm] amdgpu: 8192M of GTT memory ready.
[    1.451299] [drm] GART: num cpu pages 65536, num gpu pages 65536
[    1.451347] [drm] PCIE GART of 256M enabled (table at 0x000000F400040000).
[    1.451466] [drm] amdgpu: irq initialized.
[    1.623059] [drm] Chained IB support enabled!
[    1.624743] [drm] Found UVD firmware Version: 1.79 Family ID: 16
[    1.625444] [drm] Found VCE firmware Version: 52.4 Binary ID: 3
[    1.673073] [drm:amdgpu_mm_wdoorbell [amdgpu]] *ERROR* writing beyond doorbell aperture: 0x000001e8!
[    1.678312] [drm] DAL is enabled
[    1.678667] [drm] DM_PPLIB: values for Engine clock
[    1.678671] [drm] DM_PPLIB:	 30000
[    1.678675] [drm] DM_PPLIB:	 60800
[    1.678678] [drm] DM_PPLIB:	 91000
[    1.678681] [drm] DM_PPLIB:	 107700
[    1.678685] [drm] DM_PPLIB:	 114500
[    1.678688] [drm] DM_PPLIB:	 119100
[    1.678691] [drm] DM_PPLIB:	 123600
[    1.678695] [drm] DM_PPLIB:	 126600
[    1.678698] [drm] DM_PPLIB: Warning: using default validation clocks!
[    1.678702] [drm] DM_PPLIB: Validation clocks:
[    1.678706] [drm] DM_PPLIB:    engine_max_clock: 72000
[    1.678709] [drm] DM_PPLIB:    memory_max_clock: 80000
[    1.678713] [drm] DM_PPLIB:    level           : 0
[    1.678717] [drm] DM_PPLIB: reducing engine clock level from 8 to 2
[    1.678721] [drm] DM_PPLIB: values for Memory clock
[    1.678725] [drm] DM_PPLIB:	 30000
[    1.678728] [drm] DM_PPLIB:	 200000
[    1.678732] [drm] DM_PPLIB: Warning: using default validation clocks!
[    1.678735] [drm] DM_PPLIB: Validation clocks:
[    1.678739] [drm] DM_PPLIB:    engine_max_clock: 72000
[    1.678742] [drm] DM_PPLIB:    memory_max_clock: 80000
[    1.678746] [drm] DM_PPLIB:    level           : 0
[    1.678750] [drm] DM_PPLIB: reducing memory clock level from 2 to 1
[    1.678755] [drm] DC: create_links: connectors_num: physical:4, virtual:0
[    1.678764] [drm] Connector[0] description:signal 32
[    1.678771] [drm] Using channel: CHANNEL_ID_DDC1 [1]
[    1.678788] [drm] Connector[1] description:signal 32
[    1.678794] [drm] Using channel: CHANNEL_ID_DDC3 [3]
[    1.678810] [drm] Connector[2] description:signal 32
[    1.678815] [drm] Using channel: CHANNEL_ID_DDC2 [2]
[    1.678831] [drm] Connector[3] description:signal 4
[    1.678837] [drm] Using channel: CHANNEL_ID_DDC4 [4]
[    1.692079] [drm] Display Core initialized
[    1.692095] [drm] amdgpu: freesync_module init done ffff8800ca602700.
[    1.692603] [drm] link=0, dc_sink_in=          (null) is now Disconnected
[    1.692609] [drm] DCHPD: connector_id=0: dc_sink didn't change.
[    1.693057] [drm] link=1, dc_sink_in=          (null) is now Disconnected
[    1.693062] [drm] DCHPD: connector_id=1: dc_sink didn't change.
[    1.693490] [drm] link=2, dc_sink_in=          (null) is now Disconnected
[    1.693495] [drm] DCHPD: connector_id=2: dc_sink didn't change.
[    1.718488] [drm] [Detect]	[HDMIA][ConnIdx:3] SAMSUNG: [Block 0] 00 FF FF FF FF FF FF 00 4C 2D A4 02 00 00 00 00 2E 10 01 03 80 10 09 8C 0A E2 BD A1 5B 4A 98 24 15 47 4A A1 08 00 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 66 21 50 B0 51 00 1B 30 40 70 36 00 A0 5A 00 00 00 1E 01 1D 00 72 51 D0 1E 20 6E 28 55 00 A0 5A 00 00 00 1E 00 00 00 FD 00 31 47 0F 32 09 00 0A 20 20 20 20 20 20 00 00 00 FC 00 53 41 4D 53 55 4E 47 0A 20 20 20 20 20 01 15 ^
[    1.718522] [drm] [Detect]	[HDMIA][ConnIdx:3] SAMSUNG: [Block 1] 02 03 1A F1 46 84 13 05 14 03 12 23 09 07 07 83 01 00 00 66 03 0C 00 20 00 80 01 1D 00 BC 52 D0 1E 20 B8 28 55 40 A0 5A 00 00 00 1E 01 1D 80 18 71 1C 16 20 58 2C 25 00 A0 5A 00 00 00 9E 01 1D 80 D0 72 1C 16 20 10 2C 25 80 A0 5A 00 00 00 9E 8C 0A D0 8A 20 E0 2D 10 10 3E 96 00 A0 5A 00 00 00 18 8C 0A D0 90 20 40 31 20 0C 40 55 00 A0 5A 00 00 00 18 00 00 00 00 00 00 00 00 00 00 00 69 ^
[    1.718542] [drm] dc_link_detect: manufacturer_id = 2D4C, product_id = 2A4, serial_number = 0, manufacture_week = 46, manufacture_year = 16, display_name = SAMSUNG, speaker_flag = 1, audio_mode_count = 1
[    1.718552] [drm] dc_link_detect: mode number = 0, format_code = 1, channel_count = 1, sample_rate = 7, sample_size = 7
[    1.718559] [drm] link=3, dc_sink_in=ffff880034b69000 is now Connected
[    1.718564] [drm] DCHPD: connector_id=3: Old sink=          (null) New sink=ffff880034b69000
[    1.718588] [drm] Supports vblank timestamp caching Rev 2 (21.10.2013).
[    1.718592] [drm] Driver supports precise vblank timestamp query.
[    1.718596] [drm] KMS initialized.
[    1.721322] [drm:amdgpu_mm_wdoorbell [amdgpu]] *ERROR* writing beyond doorbell aperture: 0x00000020!
[    1.721372] [drm:amdgpu_mm_wdoorbell [amdgpu]] *ERROR* writing beyond doorbell aperture: 0x00000020!
[    1.909995] [drm:gfx_v8_0_ring_test_ring [amdgpu]] *ERROR* amdgpu: ring 0 test failed (scratch(0xC040)=0xCAFEDEAD)
[    1.910050] [drm:amdgpu_device_init [amdgpu]] *ERROR* hw_init of IP block <gfx_v8_0> failed -22
[    2.047138] [drm] amdgpu: ttm finalized
[    2.047152] [drm] amdgpu: finishing device.
```

When trying to google for the error messages like `*ERROR* writing
beyond doorbell aperture`, the only pages found were the [Linux source
code on github][5]. This makes me believe that only a few people tried
such a crazy experiment. Therefore, it would probably require a
significant effort (that may not be worth) to have this setup working.


## Giving up

After having messed around a few days (I even tried to plug the power
supply from a computer where the Radeon card is working well, with no
better outcome), I decided to plug the graphic card back to the
computer it was shipped with. At least, it is still working ; )


## Resources

* [GF7050T-M5 manual][1] is available online.
* [AMD Radeon RX 480 specifications][2] are available too.
* [Diamond AMD Radeon RX 480 specs][3] provide a bit more details.

[1]: https://www.manualslib.com/manual/451735/Ecs-Gf7050vt-M5.html
[2]: https://www.amd.com/en/products/graphics/radeon-rx-480
[3]: https://www.diamondmm.com/images/480X/RX480D58G%20%20setup%20sheet.pdf
[4]: https://en.wikipedia.org/wiki/PCI_Express
[5]: https://github.com/torvalds/linux/blob/master/drivers/gpu/drm/amd/amdgpu/amdgpu_device.c
