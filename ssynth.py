from scipy.io.wavfile import write
from numpy import linspace, sin, pi, int16
import seaborn as sns; sns.set()
import numpy as np
from scipy import signal

def tone(freq, len, amp=1, rate=44100):
    t = linspace(0, len, len*rate)
    data = sin(2*pi*freq*t) * amp
    return data

def square(freq, len, duty=0.5, amp=1, rate=44100):
    t = linspace(0, len, len*rate)
    sq = signal.square(2*pi*t*freq, duty=duty)
    return sq * amp

def sawtooth(freq, len, width=1., amp=1, rate=44100):
    t = linspace(0, len, len*rate)
    saw = signal.sawtooth(2*pi*t*freq, width)
    return saw * amp

def pause(len, rate=44100):
    t = linspace(0, 0, len*rate)
    return t

def extract_snip(tone, start, end, rate=44100):
    nsamples = len(tone)
    length = float(nsamples)/rate
    start_sample = start * rate
    end_sample = end * rate
    return tone[start_sample:end_sample]

def modulate(tone, mod):
    assert len(tone) == len(mod)
    return tone * mod

def modulate_gaussian(tone, c, rate=44100):
    nsamples = len(tone)
    length = float(nsamples)/rate
    t = linspace(-length/2, length/2, nsamples)
    #tshift = -nsamples/2
    g = np.exp(-(t)**2/(2*c**2))
    return modulate(tone, g)

def modulate_fadein(tone, in_by=0.25, rate=44100):
    nsamples = len(tone)
    length = float(nsamples)/rate
    in_by_sample = int(in_by * rate)
    t = linspace(0, 1, in_by_sample)
    nfollowing = int(nsamples - in_by_sample)
    following = linspace(1, 1, nfollowing)
    t = np.append( [t], [following] )
    return modulate(tone, t)

def modulate_fadeout(tone, start_fade=0.75, rate=44100):
    nsamples = len(tone)
    length = float(nsamples)/rate
    fade_at_sample = start_fade * rate
    nfade = int(nsamples - fade_at_sample)
    fade = linspace(1, 0, nfade)
    t = linspace(1, 1, fade_at_sample)
    t = np.append( [t], [fade] )
    return modulate(tone, t)

def modulate_parabola(tone, rate=44100):
    nsamples = len(tone)
    length = float(nsamples)/rate
    t = linspace(0, length, nsamples)
    length = length/2
    p = length**2 - (t - length)**2
    p /= np.max(p)
    return modulate(tone, p)
 

def write_waveform(data, fn, bitrate=44100):
    write(fn, bitrate, data.astype(int16))

def plot_waveform(data, fn='waveform.png'):
    sns.plt.plot(data)
    sns.plt.savefig(fn)
    sns.plt.close()

##note = tone(3000, 5, amp=10000)
###mod = tone(0.25, 2, amp=1)
###result = modulate(note, mod)
###result = modulate_gaussian(note, c=0.4)
##write_waveform(note, 'result.wav')
##plot_waveform(note)
##
##note = tone(400, 2, amp=10000)
##note = modulate_fadeout(note)
##plot_waveform(note)
##write_waveform(note, 'result2.wav')
##
##note = tone(300, 1, amp=10000)
##note = modulate_parabola(note)
##plot_waveform(note)
##write_waveform(note, 'parabola.wav')
##
##note = square(250, len=2, amp=10000)
###note = modulate_gaussian(note, c=0.2)
##note = modulate_parabola(note)
##plot_waveform(note)
##write_waveform(note, 'square.wav')
##
##note = sawtooth(250, len=2, amp=10000)
###note = modulate_gaussian(note, c=0.2)
##note = modulate_parabola(note)
##plot_waveform(note)
##write_waveform(note, 'sawtooth.wav')

###freqs = [20, 30, 40, 600]
###ifreq = 0
###silence = pause(0.15)
###audio = []
###stream = np.zeros(1)
###t = 0
###while t<30:
###    this_freq = freqs[ifreq]
###    ifreq += 1
###    if ifreq > len(freqs)-1: ifreq = 0
###    #ifreq = np.random.randint(0, len(freqs))
###    note = square(this_freq, len=1.5, amp=10000)
###    t += 1.5
###    #note = modulate_gaussian(note, c=0.2)
###    note = modulate_fadein(note, in_by=0.35)
###    audio.append(note)
###    audio.append(silence)
###    stream = np.append( stream, note )
###    stream = np.append( stream, silence )
###    t += 0.05
###
###
###audio = np.append([], audio)
###print audio.shape
###plot_waveform(stream)
###write_waveform(stream, 'audio.wav')

## 1. Establish the overall trend (volume)
#
#endtime = 120 # seconds
#dt = 1 # seconds
#t = np.linspace(0, endtime, float(endtime)/dt)
#trend = np.sin(t*50) + t/15 + np.sin(t*250)
#trend /= np.max(trend)
#trend *= 32767
#
## 2. Establish the frequencies
#
#minF = 15
#maxF = 300
#sigmaF = (maxF-minF)/10.
#ftrend = [np.random.randint(minF, maxF/10)]
#for i in range(len(t)): 
#    newF = ftrend[-1] + np.random.randn()*sigmaF
#    if newF > maxF: newF = maxF
#    if newF < minF: newF = minF
#    ftrend.append(newF)
#
#fig, ax1 = sns.plt.subplots()
#ax1.plot(trend, c='b')
#ax1.set_ylabel('Trend')
#
#ax2 = ax1.twinx()
#ax2.plot(ftrend, c='r')
#ax2.set_ylabel('Frequency (Hz)')
#sns.plt.savefig('trend.png')
#
## 3. Generate sounds
#
#stream = np.zeros(1)
#for idx_t in range(len(t)):
#    this_freq = ftrend[idx_t]
#    this_amp = trend[idx_t]
#    duration = np.random.randint(1, 6)
#    
#    silence = pause(np.random.rand()*3 + 0.1)    
#    note = square(this_freq, len=duration, amp=this_amp)
#    if np.random.randint(0, 1) == 0:
#        note = modulate_fadein(note, in_by=0.05*duration)
#    else:
#        note = modulate_gaussian(note, c=0.2)
#
#    stream = np.append( stream, note )
#    stream = np.append( stream, silence )
#
#    # for the next iteration
#    idx_t += duration - 1
#    
#plot_waveform(stream)
#write_waveform(stream, 'audio.wav')
#

####### === #######

endtime = 120 # seconds

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


