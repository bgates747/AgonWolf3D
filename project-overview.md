# Agon platform overview

## Platform architecture

The Agon Light is a standalone computer built around an eZ80 main processor and
an ESP32-PICO-D4 video display processor (VDP). The eZ80 communicates with the
VDP over a high-speed UART. The VDP handles VGA output, audio, and keyboard
input.

Stock VDP facilities include frame swapping. Assembly programs running on the
eZ80 access VDP-managed facilities through the eZ80-to-VDP communication link.

