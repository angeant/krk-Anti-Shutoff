#!/usr/bin/env python3
"""
KRK Rokit Anti-Shutoff Script
Plays an inaudible tone periodically to prevent KRK monitors from shutting off automatically.
"""

import numpy as np
import sounddevice as sd
import time
import argparse
import signal
import sys
from datetime import datetime

class KRKAntiShutoff:
    def __init__(self, frequency=10, duration=0.5, interval=25*60, volume=0.001):
        """
        Args:
            frequency (int): Tone frequency in Hz (10Hz is inaudible)
            duration (float): Tone duration in seconds
            interval (int): Interval between tones in seconds (25 min default)
            volume (float): Tone volume (very low by default)
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
    parser.add_argument('-f', '--frequency', type=int, default=10,
                       help='Tone frequency in Hz (default: 10)')
    parser.add_argument('-d', '--duration', type=float, default=0.5,
                       help='Tone duration in seconds (default: 0.5)')
    parser.add_argument('-i', '--interval', type=int, default=25,
                       help='Interval between tones in minutes (default: 25)')
    parser.add_argument('-v', '--volume', type=float, default=0.001,
                       help='Tone volume (default: 0.001)')
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
