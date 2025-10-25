#!/usr/bin/env python3
"""
生成测试音频文件的 Python 脚本
当 FFmpeg 不可用时，使用纯 Python 生成 WAV 文件
"""

import struct
import wave
import math
import os

def generate_sine_wave(filename, frequency, duration, sample_rate=44100):
    """
    生成正弦波音频文件
    
    Args:
        filename: 输出文件名（.wav）
        frequency: 频率（Hz）
        duration: 时长（秒）
        sample_rate: 采样率（默认 44100Hz）
    """
    num_samples = int(sample_rate * duration)
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(2)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        
        for i in range(num_samples):
            value = int(32767 * 0.3 * math.sin(2 * math.pi * frequency * i / sample_rate))
            packed_value = struct.pack('<hh', value, value)
            wav_file.writeframes(packed_value)
    
    return filename

def main():
    print("=" * 50)
    print("生成测试音频文件")
    print("=" * 50)
    print()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    audio_files = [
        ("scene_1_audio.wav", 440, 3.0, "场景 1"),
        ("scene_2_audio.wav", 523, 4.0, "场景 2"),
        ("scene_3_audio.wav", 659, 5.0, "场景 3"),
    ]
    
    for filename, freq, duration, desc in audio_files:
        print(f"正在生成 {filename} ({desc}, {freq}Hz, {duration}秒)...")
        try:
            generate_sine_wave(filename, freq, duration)
            file_size = os.path.getsize(filename) / 1024
            print(f"✅ {filename} ({file_size:.1f} KB)")
        except Exception as e:
            print(f"❌ 生成 {filename} 失败: {e}")
        print()
    
    print("=" * 50)
    print("✅ 所有音频文件生成完成！")
    print("=" * 50)
    print()
    print("生成的文件：")
    for filename, _, _, _ in audio_files:
        if os.path.exists(filename):
            size = os.path.getsize(filename) / 1024
            print(f"  {filename} ({size:.1f} KB)")
    print()
    print("注意：生成的是 WAV 格式文件（未压缩）")
    print("如果需要 MP3 格式，请使用 generate_audio.sh 脚本（需要 FFmpeg）")
    print()

if __name__ == "__main__":
    main()
