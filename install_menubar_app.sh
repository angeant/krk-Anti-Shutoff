#!/bin/bash
# Install KRK MenuBar App to start automatically on login

APP_NAME="KRK Anti-Shutoff"
SCRIPT_PATH="$(pwd)/krk_simple_menubar.py"
PLIST_PATH="$HOME/Library/LaunchAgents/com.krk.antishutoff.plist"

echo "🎵 Installing KRK Anti-Shutoff MenuBar App..."

# Create LaunchAgent plist file
cat > "$PLIST_PATH" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.krk.antishutoff</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>$SCRIPT_PATH</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>ProcessType</key>
    <string>Interactive</string>
    <key>LimitLoadToSessionType</key>
    <array>
        <string>Aqua</string>
    </array>
    <key>StandardOutPath</key>
    <string>$HOME/Library/Logs/krk_antishutoff.log</string>
    <key>StandardErrorPath</key>
    <string>$HOME/Library/Logs/krk_antishutoff_error.log</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>LSUIElement</key>
        <string>1</string>
    </dict>
</dict>
</plist>
EOF

# Load the LaunchAgent
launchctl load "$PLIST_PATH"

echo "✅ KRK Anti-Shutoff MenuBar App installed!"
echo "📁 LaunchAgent file: $PLIST_PATH"
echo "🚀 The app will start automatically on next login"
echo "🎯 To start now, run: python3 krk_simple_menubar.py"
echo ""
echo "To uninstall later, run:"
echo "  launchctl unload '$PLIST_PATH'"
echo "  rm '$PLIST_PATH'"
