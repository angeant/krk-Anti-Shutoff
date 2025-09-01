# KRK Rokit Anti-Shutoff

**A Python-based solution to prevent KRK Rokit studio monitors from automatically entering standby mode**

## Overview

KRK Rokit studio monitors have an auto-shutoff feature that puts them into standby mode after a period of inactivity. While this saves energy, it can be annoying for audio professionals who need their monitors to stay active during long production sessions. This project provides an elegant software solution by periodically playing inaudible tones to keep the monitors active.

## Key Features

- **🔇 Completely Inaudible**: Uses 10Hz subsonic tones that are below human hearing range
- **⚙️ Highly Configurable**: Customizable frequency, duration, interval, and volume settings  
- **🚀 Set-and-Forget**: Runs as a macOS system service with automatic startup
- **🔧 Easy Installation**: One-command setup with automated dependency management
- **📊 Monitoring**: Built-in logging and status checking capabilities
- **🧪 Test Mode**: Verify functionality before permanent installation

## How It Works

The script generates a brief (500ms) subsonic tone at 10Hz every 25 minutes. This frequency is:
- Completely inaudible to humans (below the 20Hz hearing threshold)
- Sufficient to trigger the KRK monitors' activity detection
- Low enough to not interfere with any audio production work

## Technical Specifications

- **Language**: Python 3.x
- **Dependencies**: NumPy, SoundDevice
- **Platform**: macOS (uses launchd for service management)
- **Audio Requirements**: Any audio interface or built-in audio output
- **Resource Usage**: Minimal CPU and memory footprint

## Installation & Usage

### Quick Start
```bash
cd /path/to/project
chmod +x install_krk_service.sh
./install_krk_service.sh
launchctl load ~/Library/LaunchAgents/com.user.krk-anti-shutoff.plist
```

### Manual Usage
```bash
./run_krk.sh --test        # Test mode
./run_krk.sh               # Run once
./run_krk.sh --help        # View all options
```

### Service Management
```bash
# Start service
launchctl load ~/Library/LaunchAgents/com.user.krk-anti-shutoff.plist

# Stop service  
launchctl unload ~/Library/LaunchAgents/com.user.krk-anti-shutoff.plist

# Check status
launchctl list | grep krk

# View logs
tail -f ~/.krk_anti_shutoff/krk_anti_shutoff.log
```

## Customization Options

- **Frequency**: Change the tone frequency (default: 10Hz)
- **Duration**: Adjust tone length (default: 0.5 seconds)
- **Interval**: Modify time between tones (default: 25 minutes)
- **Volume**: Control tone amplitude (default: 0.001)

Example:
```bash
./run_krk.sh --frequency 15 --interval 15 --duration 1.0
```

## Project Structure

```
krk_anti_shutoff/
├── krk_anti_shutoff.py      # Main Python script
├── install_krk_service.sh   # Automated installer
├── run_krk.sh              # Simple execution wrapper
├── requirements.txt        # Python dependencies
└── README_KRK.md          # Detailed documentation
```

## Use Cases

- **Professional Studios**: Keep monitors active during long mixing/mastering sessions
- **Home Studios**: Eliminate the annoyance of monitors shutting off during creative work
- **Live Streaming**: Ensure consistent audio monitoring during broadcasts
- **Audio Production**: Maintain workflow continuity without interruption

## Benefits

- **Non-Invasive**: No hardware modifications required
- **Reversible**: Easy to enable/disable or completely remove
- **Energy Conscious**: Uses minimal system resources
- **Professional**: Designed by audio engineers for audio engineers

## Compatibility

- **KRK Models**: Works with all KRK Rokit generations (G3, G4, G5, RP series)
- **Operating System**: macOS (with potential for Linux/Windows adaptation)
- **Audio Interfaces**: Compatible with any Core Audio device

## Contributing

This project addresses a common pain point in the audio production community. Contributions for additional features, platform support, or optimizations are welcome.

---

*Created for the audio production community by audio engineers who understand the workflow interruptions caused by auto-shutoff features.*
