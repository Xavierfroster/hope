import wave
import struct
import math
import os

def apply_optimus_effect(input_wav_path, output_wav_path):
    """
    Applies an offline Optimus Prime DSP voice effect to a standard WAV file.
    
    1. Pitch Shift (Resampling): Lowers the samplerate in the header to 65%, 
       making the voice deep and authoritative (offsetting the fast synthesised input).
    2. Metallic Comb Filter: Uses IIR feedback (~12ms delay) to add mechanical resonance.
    3. Reverb/Chest Echo: Uses a secondary longer delay (~80ms) for a robotic giant tone.
    4. LFO Ring Modulation: Uses a 42Hz sine wave to add mechanical vibration/growl.
    """
    if not os.path.exists(input_wav_path):
        raise FileNotFoundError(f"Input WAV not found: {input_wav_path}")
        
    with wave.open(input_wav_path, 'rb') as infile:
        params = infile.getparams()
        nchannels, sampwidth, framerate, nframes, comptype, compname = params
        raw_frames = infile.readframes(nframes)
    
    # Pitch shift factor (0.65 lowers the pitch by a perfect fourth/fifth)
    pitch_factor = 0.65
    new_framerate = int(framerate * pitch_factor)
    
    # Decode samples to signed integers
    if sampwidth == 2:
        num_samples = len(raw_frames) // 2
        samples = list(struct.unpack(f"<{num_samples}h", raw_frames))
    elif sampwidth == 1:
        num_samples = len(raw_frames)
        samples = [s - 128 for s in struct.unpack(f"<{num_samples}B", raw_frames)]
    else:
        # Unsupported format (e.g. 24-bit/32-bit float), fallback to direct copy
        with wave.open(output_wav_path, 'wb') as outfile:
            outfile.setparams(params)
            outfile.writeframes(raw_frames)
        return

    # Processing buffers
    processed = [0] * len(samples)
    
    # DSP Coefficients
    # 1. Comb Filter (metallic ring)
    comb_delay_sec = 0.013 # 13 ms
    comb_delay = int(new_framerate * comb_delay_sec) * nchannels
    comb_feedback = 0.52
    
    # 2. Chest Echo (mechanical body resonance)
    echo_delay_sec = 0.080 # 80 ms
    echo_delay = int(new_framerate * echo_delay_sec) * nchannels
    echo_feedback = 0.18
    
    # 3. LFO Ring Modulator
    lfo_freq = 42.0 # Hz
    lfo_depth = 0.16 # Modulation depth
    
    for i in range(len(samples)):
        val = samples[i]
        
        # Apply Comb Filter
        out_val = val
        if i >= comb_delay:
            out_val += int(processed[i - comb_delay] * comb_feedback)
            
        # Apply Chest Reverb/Echo
        if i >= echo_delay:
            out_val += int(processed[i - echo_delay] * echo_feedback)
            
        # Clamp to 16-bit range
        if out_val > 32767:
            out_val = 32767
        elif out_val < -32768:
            out_val = -32768
            
        # Apply LFO Ring Modulation
        sample_idx = i // nchannels
        t = sample_idx / new_framerate
        modulation = 1.0 + lfo_depth * math.sin(2.0 * math.pi * lfo_freq * t)
        modulated_val = int(out_val * modulation)
        
        # Final Clamp
        if modulated_val > 32767:
            modulated_val = 32767
        elif modulated_val < -32768:
            modulated_val = -32768
            
        processed[i] = modulated_val
        
    # Re-encode samples
    if sampwidth == 2:
        out_frames = struct.pack(f"<{len(processed)}h", *processed)
    else:
        out_frames = struct.pack(f"<{len(processed)}B", *[s + 128 for s in processed])
        
    # Write output WAV file
    with wave.open(output_wav_path, 'wb') as outfile:
        outfile.setparams((nchannels, sampwidth, new_framerate, len(processed) // nchannels, comptype, compname))
        outfile.writeframes(out_frames)
