#!/bin/bash

# Installation script for KRK Anti-Shutoff
echo "🎵 Installing KRK Rokit Anti-Shutoff..."

# Verify Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Create directory for the service
SERVICE_DIR="$HOME/.krk_anti_shutoff"
mkdir -p "$SERVICE_DIR"

# Copy files
cp krk_anti_shutoff.py "$SERVICE_DIR/"
cp requirements.txt "$SERVICE_DIR/"

# Create virtual environment and install dependencies
echo "📦 Creating virtual environment and installing dependencies..."
python3 -m venv "$SERVICE_DIR/venv"
source "$SERVICE_DIR/venv/bin/activate"
pip install -r "$SERVICE_DIR/requirements.txt"

# Create plist file for launchd
PLIST_FILE="$HOME/Library/LaunchAgents/com.user.krk-anti-shutoff.plist"

cat > "$PLIST_FILE" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.user.krk-anti-shutoff</string>
    <key>ProgramArguments</key>
    <array>
        <string>$SERVICE_DIR/venv/bin/python</string>
        <string>$SERVICE_DIR/krk_anti_shutoff.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>$SERVICE_DIR/krk_anti_shutoff.log</string>
    <key>StandardErrorPath</key>
    <string>$SERVICE_DIR/krk_anti_shutoff_error.log</string>
    <key>WorkingDirectory</key>
    <string>$SERVICE_DIR</string>
</dict>
</plist>
EOF

# Make script executable
chmod +x "$SERVICE_DIR/krk_anti_shutoff.py"

echo "✅ Installation completed!"
echo ""
echo "To use the service:"
echo "  Start: launchctl load $PLIST_FILE"
echo "  Stop: launchctl unload $PLIST_FILE"
echo "  View logs: tail -f $SERVICE_DIR/krk_anti_shutoff.log"
echo ""
echo "For manual usage:"
echo "  python3 $SERVICE_DIR/krk_anti_shutoff.py"
echo "  python3 $SERVICE_DIR/krk_anti_shutoff.py --test"
echo "  python3 $SERVICE_DIR/krk_anti_shutoff.py --help"
