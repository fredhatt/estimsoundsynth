import numpy as np
from ssynth import *

# 1. Establish the overall trend (volume)

endtime = 120 # seconds
dt = 1 # seconds
t = np.linspace(0, endtime, float(endtime)/dt)
trend = np.sin(t*50) + t/15 + np.sin(t*250)
trend /= np.max(trend)
trend *= 32767

# 2. Establish the frequencies

minF = 15
maxF = 300
sigmaF = (maxF-minF)/10.
ftrend = [np.random.randint(minF, maxF/10)]
for i in range(len(t)): 
    newF = ftrend[-1] + np.random.randn()*sigmaF
    if newF > maxF: newF = maxF
    if newF < minF: newF = minF
    ftrend.append(newF)

fig, ax1 = sns.plt.subplots()
ax1.plot(trend, c='b')
ax1.set_ylabel('Trend')

ax2 = ax1.twinx()
ax2.plot(ftrend, c='r')
ax2.set_ylabel('Frequency (Hz)')
sns.plt.savefig('trend.png')

# 3. Generate sounds

stream = np.zeros(1)
for idx_t in range(len(t)):
    this_freq = ftrend[idx_t]
    this_amp = trend[idx_t]
    duration = np.random.randint(1, 6)
    
    silence = pause(np.random.rand()*3 + 0.1)    
    note = square(this_freq, len=duration, amp=this_amp)
    if np.random.randint(0, 1) == 0:
        note = modulate_fadein(note, in_by=0.05*duration)
    else:
        note = modulate_gaussian(note, c=0.2)

    stream = np.append( stream, note )
    stream = np.append( stream, silence )

    # for the next iteration
    idx_t += duration - 1
    
plot_waveform(stream)
write_waveform(stream, 'audio.wav')


