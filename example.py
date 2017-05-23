import numpy as np
from ssynth import *


# presets
rumble_low = square(15, len=6, amp=10000)
rumble = square(40, len=6, amp=10000)
rumble_mid = square(100, len=6, amp=10000)
rumble_high = square(150, len=5, amp=10000)
spike = tone(2000, len=4, amp=15000)
rampup = modulate_fadein(sawtooth(100, len=30, amp=12500), in_by=27)
pulse_high = modulate_parabola(tone(1500, len=2, amp=20000))
pulse_low = modulate_parabola(tone(200, len=2, amp=12500))


p0 = pause(0.25)
p1 = pause(1)
p2 = pause(2)
p3 = pause(3)

stream = np.zeros(1)
stream = np.append(stream, rumble)
stream = np.append(stream, p1)

stream = np.append(stream, rumble_low)
stream = np.append(stream, p0)

stream = np.append(stream, rumble_mid)
stream = np.append(stream, spike)
#stream = np.append(stream, p0)

stream = np.append(stream, rumble_mid)
stream = np.append(stream, spike)
#stream = np.append(stream, p0)

stream = np.append(stream, rumble_mid)
stream = np.append(stream, spike)

stream = np.append(stream, p1)
stream = np.append(stream, pulse_high)
stream = np.append(stream, pulse_low)

stream = np.append(stream, p1)
stream = np.append(stream, rampup)

stream = np.append(stream, p1)
stream = np.append(stream, rampup)

stream = np.append(stream, p1)
stream = np.append(stream, rampup)

stream = np.append(stream, p1)
stream = np.append(stream, rampup)

stream = np.append(stream, p1)
stream = np.append(stream, rampup)


#plot_waveform(stream)
write_waveform(stream, 'audio.wav')

