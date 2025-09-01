# KRK Rokit Anti-Shutoff

Python script to prevent KRK Rokit studio monitors from automatically shutting off by periodically playing an inaudible tone.

## 🚀 Quick Installation

```bash
cd "/Users/angeloantonelli/Documents/Coding Projects"
chmod +x install_krk_service.sh
./install_krk_service.sh
```

## 📋 Manual Usage

### Run once:
```bash
./run_krk.sh
```

### Test that it works:
```bash
./run_krk.sh --test
```

### Customize configuration:
```bash
# Change interval to 15 minutes
./run_krk.sh --interval 15

# Change frequency to 20Hz
./run_krk.sh --frequency 20

# View all options
./run_krk.sh --help
```

### Alternative (manual):
```bash
# Activate virtual environment
source krk_venv/bin/activate

# Run script
python3 krk_anti_shutoff.py --test
```

## 🔧 As Service (Runs Automatically)

### Start service:
```bash
launchctl load ~/Library/LaunchAgents/com.user.krk-anti-shutoff.plist
```

### Stop service:
```bash
launchctl unload ~/Library/LaunchAgents/com.user.krk-anti-shutoff.plist
```

### Check if running:
```bash
launchctl list | grep krk-anti-shutoff
```

### View logs:
```bash
tail -f ~/.krk_anti_shutoff/krk_anti_shutoff.log
```

## ⚙️ Configuration

By default the script:
- Plays a **50Hz** tone (subsonic, completely inaudible, based on original Reddit hack)
- For **1.2 seconds**
- Every **25 minutes**
- At moderate volume (**0.3** - safe for subsonic frequencies)

You can change these values with parameters:
- `--frequency` (-f): Frequency in Hz
- `--duration` (-d): Duration in seconds  
- `--interval` (-i): Interval in minutes
- `--volume` (-v): Volume (0.001 - 1.0)

## 🛠 Troubleshooting

### Error "No module named sounddevice":
```bash
pip3 install sounddevice numpy
```

### Error "No audio device found":
Verify that your audio interface is connected and configured as the default output in System Preferences > Sound.

### Service doesn't start automatically:
```bash
# Check permissions
ls -la ~/Library/LaunchAgents/com.user.krk-anti-shutoff.plist

# Reload service
launchctl unload ~/Library/LaunchAgents/com.user.krk-anti-shutoff.plist
launchctl load ~/Library/LaunchAgents/com.user.krk-anti-shutoff.plist
```

## 🎯 How Does It Work?

The script plays a 50Hz tone (subsonic frequency, completely inaudible to humans) every 25 minutes. This implementation is based on the original Reddit hack from r/audioengineering. The signal is strong enough for KRK monitors to detect activity and prevent them from entering automatic standby mode, while remaining completely silent to human ears.

## 📁 Created Files

- `~/.krk_anti_shutoff/krk_anti_shutoff.py` - Main script
- `~/.krk_anti_shutoff/krk_anti_shutoff.log` - Service logs
- `~/Library/LaunchAgents/com.user.krk-anti-shutoff.plist` - Service configuration
