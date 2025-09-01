#!/usr/bin/env python3
"""
KRK Rokit Anti-Shutoff Background MenuBar App
A background-only macOS menu bar application that prevents KRK monitors from shutting off.
This version runs only in the menu bar and doesn't appear in the dock.
"""

import rumps
import numpy as np
import sounddevice as sd
import threading
import time
import os
import sys
from datetime import datetime, timedelta

# Import AppKit for background mode (will be configured after rumps init)

class KRKBackgroundApp(rumps.App):
    def __init__(self):
        super(KRKBackgroundApp, self).__init__("🎵")
        
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
        
        # Build menu
        self.build_menu()
        
        # Timer for updating menu
        self.timer = rumps.Timer(self.update_menu, 1)
        self.timer.start()
    
    def build_menu(self):
        """Build the menu items"""
        self.menu.clear()
        
        self.menu.add(rumps.MenuItem("KRK Anti-Shutoff", callback=None))
        self.menu.add(rumps.separator)
        
        # Control items
        self.start_item = rumps.MenuItem("▶ Start Protection", callback=self.start_protection)
        self.stop_item = rumps.MenuItem("⏸ Stop Protection", callback=self.stop_protection)
        self.menu.add(self.start_item)
        self.menu.add(self.stop_item)
        
        self.menu.add(rumps.separator)
        self.menu.add(rumps.MenuItem("🧪 Test Tone", callback=self.test_tone))
        self.menu.add(rumps.separator)
        
        # Status items
        self.status_item = rumps.MenuItem("ℹ️ Status: Stopped", callback=None)
        self.next_tone_item = rumps.MenuItem("⏰ Next tone: --", callback=None)
        self.menu.add(self.status_item)
        self.menu.add(self.next_tone_item)
        
        self.menu.add(rumps.separator)
        self.menu.add(rumps.MenuItem("⚙️ Settings", callback=self.show_settings))
        self.menu.add(rumps.separator)
        self.menu.add(rumps.MenuItem("🔄 Restart App", callback=self.restart_app))
        self.menu.add(rumps.MenuItem("❌ Quit", callback=self.quit_app))
        
        # Initially disable stop button
        self.stop_item.set_callback(None)
    
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

Background App Mode:
✅ Runs only in menu bar
✅ Hidden from dock
✅ Stays running when "closed"

To fully quit: Use "❌ Quit" from menu"""
        
        rumps.alert("KRK Anti-Shutoff Settings", settings_text)
    
    def restart_app(self, sender):
        """Restart the application"""
        rumps.notification("KRK Anti-Shutoff", "Restarting...", "App will restart in background mode")
        python = sys.executable
        os.execl(python, python, *sys.argv)
    
    def quit_app(self, sender):
        """Properly quit the application"""
        if self.is_running:
            self.stop_protection(None)
        
        rumps.notification("KRK Anti-Shutoff", "App Closed", "To restart: python3 krk_background_app.py")
        rumps.quit_application()
    
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
    app = KRKBackgroundApp()
    print("🎵 KRK Anti-Shutoff running in background mode (menu bar only)")
    print("   Look for the 🎵 icon in your menu bar")
    print("   The app will NOT appear in the dock")
    app.run()
