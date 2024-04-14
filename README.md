# gd32f103cbt6-rdp-testing
Stuff for testing swd debugging on a gd32f103cbt6.

## stuff 2 know
Flash size: 0x20000 == 128kB
NRST 1 OR GND 
BOOT 0 1
BOOT 1 (PA2) 1
chip.dap dpreg 0x4 0x0

## openocd
jlink
select transport swd
openocd -f interface/jlink.cfg -f target/stm32f1x.cfg

## telnet
host: localhost
port: 4444



