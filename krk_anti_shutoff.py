#!/usr/bin/env python3
"""
KRK Rokit Anti-Shutoff Script
Plays an inaudible tone periodically to prevent KRK monitors from shutting off automatically.

Based on the original hack from r/audioengineering:
https://www.reddit.com/r/audioengineering/comments/8hmsgh/i_made_a_hack_to_stop_krk_rokits_from_auto/
Original implementation: https://pastebin.com/PwudtYbZ
"""

import numpy as np
import sounddevice as sd
import time
import argparse
import signal
import sys
from datetime import datetime

class KRKAntiShutoff:
    def __init__(self, frequency=50, duration=3.0, interval=25*60, volume=0.8):
        """
        Args:
            frequency (int): Tone frequency in Hz (50Hz is inaudible, based on original Reddit hack)
            duration (float): Tone duration in seconds (3.0s for reliable wake-up)
            interval (int): Interval between tones in seconds (25 min default)
            volume (float): Tone volume (0.8 default - higher volume for reliable wake-up)
        """
        self.frequency = frequency
        self.duration = duration
        self.interval = interval
        self.volume = volume
        self.running = True
        self.sample_rate = 44100
        
        # Configure signal handling for clean exit
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        """Handles interrupt signal for clean exit"""
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Stopping KRK Anti-Shutoff...")
        self.running = False
        sys.exit(0)
    
    def generate_tone(self):
        """Generates a tone at the specified frequency"""
        samples = int(self.sample_rate * self.duration)
        t = np.linspace(0, self.duration, samples, False)
        # Generate sine wave
        wave = np.sin(2 * np.pi * self.frequency * t) * self.volume
        return wave
    
    def play_tone(self):
        """Plays the inaudible tone"""
        try:
            tone = self.generate_tone()
            sd.play(tone, samplerate=self.sample_rate)
            sd.wait()  # Wait for playback to finish
            return True
        except Exception as e:
            print(f"Error playing tone: {e}")
            return False
    
    def run(self):
        """Runs the main loop"""
        print("🎵 KRK Rokit Anti-Shutoff started")
        print(f"   Frequency: {self.frequency}Hz")
        print(f"   Duration: {self.duration}s")
        print(f"   Interval: {self.interval//60} minutes")
        print(f"   Volume: {self.volume}")
        print("   Press Ctrl+C to stop\n")
        
        while self.running:
            current_time = datetime.now().strftime('%H:%M:%S')
            print(f"[{current_time}] Playing inaudible tone to keep KRK monitors active...")
            
            if self.play_tone():
                print(f"[{current_time}] ✅ Tone played successfully")
            else:
                print(f"[{current_time}] ❌ Error playing tone")
            
            print(f"[{current_time}] 💤 Waiting {self.interval//60} minutes until next tone...\n")
            
            # Wait for specified interval
            time.sleep(self.interval)

def main():
    parser = argparse.ArgumentParser(description='KRK Rokit Anti-Shutoff Script')
    parser.add_argument('-f', '--frequency', type=int, default=50,
                       help='Tone frequency in Hz (default: 50, like original Reddit hack)')
    parser.add_argument('-d', '--duration', type=float, default=3.0,
                       help='Tone duration in seconds (default: 3.0)')
    parser.add_argument('-i', '--interval', type=int, default=25,
                       help='Interval between tones in minutes (default: 25)')
    parser.add_argument('-v', '--volume', type=float, default=0.8,
                       help='Tone volume (default: 0.8 - higher volume for reliable wake-up)')
    parser.add_argument('--test', action='store_true',
                       help='Test mode: play one tone and exit')
    
    args = parser.parse_args()
    
    # Convert interval from minutes to seconds
    interval_seconds = args.interval * 60
    
    anti_shutoff = KRKAntiShutoff(
        frequency=args.frequency,
        duration=args.duration,
        interval=interval_seconds,
        volume=args.volume
    )
    
    if args.test:
        print("🧪 Test mode: playing one tone...")
        if anti_shutoff.play_tone():
            print("✅ Test successful - tone played correctly")
        else:
            print("❌ Test failed - error playing tone")
        return
    
    try:
        anti_shutoff.run()
    except KeyboardInterrupt:
        print("\n🛑 Script stopped by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
