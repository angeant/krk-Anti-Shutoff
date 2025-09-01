#!/usr/bin/env python3
"""
KRK Rokit Anti-Shutoff Simple MenuBar App
A simple, reliable macOS menu bar application for KRK monitor protection.
"""

import rumps
import numpy as np
import sounddevice as sd
import threading
import time
import os
import sys
from datetime import datetime, timedelta

class KRKSimpleApp(rumps.App):
    def __init__(self):
        super(KRKSimpleApp, self).__init__("🎵")
        
        # Settings that work
        self.frequency = 50
        self.duration = 3.0
        self.interval = 25 * 60  # 25 minutes
        self.volume = 0.8
        self.sample_rate = 44100
        
        # State
        self.is_running = False
        self.worker_thread = None
        self.next_tone_time = None
        
        # Build menu
        self.setup_menu()
        
        # Update timer
        self.timer = rumps.Timer(self.update_status, 1)
        self.timer.start()
        
        # Auto-start protection
        rumps.notification("KRK Anti-Shutoff", "Started", "Ready to protect your monitors! 🎵")
    
    def setup_menu(self):
        """Setup menu items"""
        self.menu = [
            rumps.MenuItem("🎵 KRK Anti-Shutoff", callback=None),
            rumps.separator,
            "▶ Start Protection",
            "⏸ Stop Protection", 
            rumps.separator,
            "🧪 Test Tone",
            rumps.separator,
            rumps.MenuItem("Status: Stopped 🔴", callback=None),
            rumps.MenuItem("Next: --", callback=None),
            rumps.separator,
            "❌ Quit"
        ]
        
        # Disable stop initially
        self.menu["⏸ Stop Protection"].set_callback(None)
    
    @rumps.clicked("▶ Start Protection")
    def start_protection(self, _):
        """Start protection"""
        self.is_running = True
        self.worker_thread = threading.Thread(target=self.worker_loop, daemon=True)
        self.worker_thread.start()
        
        # Update menu
        self.menu["▶ Start Protection"].set_callback(None)
        self.menu["⏸ Stop Protection"].set_callback(self.stop_protection)
        self.title = "🎵🟢"
        
        rumps.notification("KRK Protection", "Started", "Playing tones every 25 minutes")
    
    @rumps.clicked("⏸ Stop Protection")  
    def stop_protection(self, _):
        """Stop protection"""
        self.is_running = False
        self.next_tone_time = None
        
        # Update menu
        self.menu["▶ Start Protection"].set_callback(self.start_protection)
        self.menu["⏸ Stop Protection"].set_callback(None)
        self.title = "🎵"
        
        rumps.notification("KRK Protection", "Stopped", "Monitors may sleep now")
    
    @rumps.clicked("🧪 Test Tone")
    def test_tone(self, _):
        """Test tone"""
        def play_test():
            success = self.play_tone()
            if success:
                rumps.notification("Test", "✅ Success", f"{self.frequency}Hz for {self.duration}s")
            else:
                rumps.notification("Test", "❌ Failed", "Check audio settings")
        
        threading.Thread(target=play_test, daemon=True).start()
    
    @rumps.clicked("❌ Quit")
    def quit_app(self, _):
        """Quit app"""
        self.is_running = False
        rumps.quit_application()
    
    def play_tone(self):
        """Play the tone"""
        try:
            samples = int(self.sample_rate * self.duration)
            t = np.linspace(0, self.duration, samples, False)
            tone = np.sin(2 * np.pi * self.frequency * t) * self.volume
            sd.play(tone, samplerate=self.sample_rate)
            sd.wait()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    def worker_loop(self):
        """Main protection loop"""
        while self.is_running:
            # Play tone
            current_time = datetime.now()
            success = self.play_tone()
            
            if success:
                print(f"[{current_time.strftime('%H:%M:%S')}] ✅ Tone played")
            
            # Set next time
            self.next_tone_time = current_time + timedelta(seconds=self.interval)
            
            # Wait (check every second for stop)
            for _ in range(self.interval):
                if not self.is_running:
                    break
                time.sleep(1)
    
    def update_status(self, _):
        """Update status in menu"""
        if self.is_running:
            self.menu["Status: Stopped 🔴"].title = "Status: Running 🟢"
            
            if self.next_tone_time:
                remaining = self.next_tone_time - datetime.now()
                if remaining.total_seconds() > 0:
                    mins = int(remaining.total_seconds() // 60)
                    secs = int(remaining.total_seconds() % 60)
                    self.menu["Next: --"].title = f"Next: {mins:02d}:{secs:02d}"
                else:
                    self.menu["Next: --"].title = "Next: Playing..."
            else:
                self.menu["Next: --"].title = "Next: Soon..."
        else:
            self.menu["Status: Stopped 🔴"].title = "Status: Stopped 🔴"
            self.menu["Next: --"].title = "Next: --"

if __name__ == "__main__":
    print("🎵 Starting KRK Anti-Shutoff MenuBar App...")
    KRKSimpleApp().run()
