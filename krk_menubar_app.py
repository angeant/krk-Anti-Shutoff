#!/usr/bin/env python3
"""
KRK Rokit Anti-Shutoff MenuBar App
A macOS menu bar application that prevents KRK monitors from shutting off automatically.
"""

import rumps
import numpy as np
import sounddevice as sd
import threading
import time
from datetime import datetime, timedelta

class KRKMenuBarApp(rumps.App):
    def __init__(self):
        super(KRKMenuBarApp, self).__init__("🎵", quit_button=None)
        
        # Default settings that worked for your speakers
        self.frequency = 50  # Hz
        self.duration = 3.0  # seconds
        self.interval = 25 * 60  # 25 minutes in seconds
        self.volume = 0.8
        self.sample_rate = 44100
        
        # App state
        self.is_running = False
        self.worker_thread = None
        self.next_tone_time = None
        
        # Menu items
        self.menu = [
            rumps.MenuItem("KRK Anti-Shutoff", callback=None),
            rumps.separator,
            rumps.MenuItem("▶ Start Protection", callback=self.start_protection),
            rumps.MenuItem("⏸ Stop Protection", callback=self.stop_protection),
            rumps.separator,
            rumps.MenuItem("🧪 Test Tone", callback=self.test_tone),
            rumps.separator,
            rumps.MenuItem("ℹ️ Status: Stopped", callback=None),
            rumps.MenuItem("⏰ Next tone: --", callback=None),
            rumps.separator,
            rumps.MenuItem("⚙️ Settings", callback=self.show_settings),
            rumps.separator,
            rumps.MenuItem("❌ Quit", callback=rumps.quit_application),
        ]
        
        # Update menu item references
        self.start_item = self.menu["▶ Start Protection"]
        self.stop_item = self.menu["⏸ Stop Protection"]
        self.status_item = self.menu["ℹ️ Status: Stopped"]
        self.next_tone_item = self.menu["⏰ Next tone: --"]
        
        # Initially disable stop button
        self.stop_item.set_callback(None)
        
        # Timer for updating menu
        self.timer = rumps.Timer(self.update_menu, 1)
        self.timer.start()
    
    def generate_tone(self):
        """Generates a tone at the specified frequency"""
        samples = int(self.sample_rate * self.duration)
        t = np.linspace(0, self.duration, samples, False)
        wave = np.sin(2 * np.pi * self.frequency * t) * self.volume
        return wave
    
    def play_tone(self):
        """Plays the inaudible tone"""
        try:
            tone = self.generate_tone()
            sd.play(tone, samplerate=self.sample_rate)
            sd.wait()
            return True
        except Exception as e:
            print(f"Error playing tone: {e}")
            return False
    
    def worker_function(self):
        """Main worker function that runs in background thread"""
        while self.is_running:
            current_time = datetime.now()
            
            # Play tone
            success = self.play_tone()
            
            if success:
                print(f"[{current_time.strftime('%H:%M:%S')}] ✅ Tone played successfully")
            else:
                print(f"[{current_time.strftime('%H:%M:%S')}] ❌ Error playing tone")
            
            # Calculate next tone time
            self.next_tone_time = current_time + timedelta(seconds=self.interval)
            
            # Wait for specified interval (but check every second if we should stop)
            for _ in range(self.interval):
                if not self.is_running:
                    break
                time.sleep(1)
    
    def start_protection(self, sender):
        """Start the anti-shutoff protection"""
        if not self.is_running:
            self.is_running = True
            self.worker_thread = threading.Thread(target=self.worker_function, daemon=True)
            self.worker_thread.start()
            
            # Update menu
            self.start_item.set_callback(None)
            self.stop_item.set_callback(self.stop_protection)
            self.title = "🎵🟢"  # Green indicator
            
            rumps.notification("KRK Anti-Shutoff", "Protection Started", 
                             f"Playing {self.frequency}Hz tone every {self.interval//60} minutes")
    
    def stop_protection(self, sender):
        """Stop the anti-shutoff protection"""
        if self.is_running:
            self.is_running = False
            if self.worker_thread:
                self.worker_thread.join(timeout=2)
            
            # Reset next tone time
            self.next_tone_time = None
            
            # Update menu
            self.start_item.set_callback(self.start_protection)
            self.stop_item.set_callback(None)
            self.title = "🎵"  # Normal indicator
            
            rumps.notification("KRK Anti-Shutoff", "Protection Stopped", "Monitors may auto-shutoff now")
    
    def test_tone(self, sender):
        """Play a test tone"""
        def test_in_background():
            success = self.play_tone()
            if success:
                rumps.notification("KRK Test", "✅ Test Successful", 
                                 f"Played {self.frequency}Hz tone for {self.duration}s")
            else:
                rumps.notification("KRK Test", "❌ Test Failed", "Error playing tone")
        
        # Run test in background thread to avoid blocking UI
        test_thread = threading.Thread(target=test_in_background, daemon=True)
        test_thread.start()
    
    def show_settings(self, sender):
        """Show settings dialog"""
        settings_text = f"""Current Settings:
        
• Frequency: {self.frequency} Hz
• Duration: {self.duration} seconds  
• Interval: {self.interval//60} minutes
• Volume: {self.volume}

These settings worked for your KRK speakers. 
You can modify them by editing the script if needed."""
        
        rumps.alert("KRK Anti-Shutoff Settings", settings_text)
    
    def update_menu(self, sender):
        """Update menu items with current status"""
        if self.is_running:
            self.status_item.title = "ℹ️ Status: Running 🟢"
            
            if self.next_tone_time:
                remaining = self.next_tone_time - datetime.now()
                if remaining.total_seconds() > 0:
                    minutes = int(remaining.total_seconds() // 60)
                    seconds = int(remaining.total_seconds() % 60)
                    self.next_tone_item.title = f"⏰ Next tone: {minutes:02d}:{seconds:02d}"
                else:
                    self.next_tone_item.title = "⏰ Next tone: Playing..."
            else:
                self.next_tone_item.title = "⏰ Next tone: Soon..."
        else:
            self.status_item.title = "ℹ️ Status: Stopped 🔴"
            self.next_tone_item.title = "⏰ Next tone: --"

if __name__ == "__main__":
    app = KRKMenuBarApp()
    app.run()
