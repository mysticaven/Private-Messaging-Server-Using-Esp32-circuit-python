# Private-Messaging-Server-Using-Esp32-circuit-python

# 💬 ESP32 Real-Time Chat Application

> A beautiful, lightweight chat application running entirely on an ESP32 microcontroller with DaisyUI styling!

![ESP32](https://img.shields.io/badge/ESP32-000000?style=for-the-badge&logo=espressif&logoColor=white)
![CircuitPython](https://img.shields.io/badge/CircuitPython-blueviolet?style=for-the-badge&logo=python&logoColor=white)
![DaisyUI](https://img.shields.io/badge/DaisyUI-5A0EF8?style=for-the-badge&logo=daisyui&logoColor=white)

## ✨ What I Built

I created a fully functional real-time chat server that runs directly on an ESP32 microcontroller! No cloud servers, no databases—just pure embedded magic. 🪄

### 🎯 Features

- 🔐 **User Authentication** - Custom username login system
- 👥 **Multi-User Support** - Up to 5 concurrent users
- 🔄 **Smart Auto-Refresh** - Refreshes every 3 seconds, but pauses when you're typing
- ⏰ **Self-Destructing Messages** - Messages automatically vanish after 20 seconds
- 🎨 **Beautiful UI** - Modern DaisyUI components with the "Cupcake" theme
- 📱 **Responsive Design** - Works perfectly on mobile and desktop
- 🚀 **Lightweight** - Runs on microcontroller with <5KB RAM usage
- 💾 **In-Memory Storage** - All data stored in RAM (no persistent storage)

## 🛠️ Technical Stack

- **Hardware**: ESP32 microcontroller
- **Language**: CircuitPython
- **Backend**: Custom HTTP server with socket programming
- **Frontend**: HTML5 + DaisyUI + Tailwind CSS
- **Networking**: Wi-Fi direct connection

## 🎨 UI Highlights

### Login Page
- Gradient background (purple to indigo)
- User count badge showing online users
- Full/available status indicator
- Clean, modern card design

### Chat Interface
- WhatsApp-style chat bubbles
- Navbar with online user dropdown
- Auto-scrolling message area
- Send button with icon
- Exit button to leave chat

## 🧠 How It Works

### Architecture
```
ESP32 (Port 80) ← HTTP Request ← User's Browser
       ↓
   Socket Server
       ↓
   Message Handler (RAM Storage)
       ↓
   HTML Response → User's Browser
```

### Key Components

1. **Wi-Fi Connection**: Connects to your home network
2. **Socket Server**: Listens on port 80 for HTTP requests
3. **Message Storage**: In-memory list with timestamps
4. **URL Parser**: Custom URL decoder for CircuitPython
5. **HTML Generator**: Dynamic page generation with user data
6. **Session Manager**: Tracks users by IP address

### Smart Features

**Auto-Cleanup System**
- Messages older than 20 seconds are automatically deleted
- Keeps maximum 20 messages in memory
- Runs on every page render

**Non-Intrusive Refresh**
- JavaScript detects when user is typing
- Pauses auto-refresh during typing
- Resumes 500ms after last keystroke
- Prevents message loss while composing

**Resource Optimization**
- 1KB buffer for network data
- Efficient string operations
- Minimal memory allocation
- Connection pooling with timeout

## 🚀 Setup & Usage

### Hardware Requirements
- ESP32 development board
- USB cable for power/programming
- Wi-Fi network

### Software Requirements
- CircuitPython installed on ESP32
- Environment variables set:
  - `CIRCUITPY_WIFI_SSID`
  - `CIRCUITPY_WIFI_PASSWORD`

### Running the App

1. **Upload** `code.py` to your ESP32
2. **Reset** the board
3. **Check** serial output for IP address
4. **Visit** `http://[ESP32_IP]` in your browser
5. **Enter** your name and start chatting!

## 📊 Technical Specifications

| Metric | Value |
|--------|-------|
| Max Users | 5 concurrent |
| Max Messages | 20 stored |
| Message TTL | 20 seconds |
| Refresh Rate | 3 seconds |
| Buffer Size | 1024 bytes |
| Port | 80 (HTTP) |
| Memory Usage | ~5KB RAM |

## 🎯 Challenges Solved

### 1. **No localStorage Support**
- **Problem**: Browser storage not available in artifact environment
- **Solution**: Used in-memory storage with timestamps

### 2. **Limited RAM**
- **Problem**: ESP32 has only ~520KB total RAM
- **Solution**: Circular buffer with 20 message limit + auto-cleanup

### 3. **CircuitPython Limitations**
- **Problem**: No `urllib.parse` module
- **Solution**: Custom URL decoder implementation

### 4. **Socket API Differences**
- **Problem**: CircuitPython uses `recv_into()` instead of `recv()`
- **Solution**: Pre-allocated buffer with `recv_into()`

### 5. **Refresh During Typing**
- **Problem**: Auto-refresh interrupts message composition
- **Solution**: JavaScript event listeners to detect typing state

## 🔒 Security Features

- **HTML Escaping**: Prevents XSS injection attacks
- **Input Validation**: Username and message length limits
- **User Limit**: Maximum 5 users prevents resource exhaustion
- **Timeout Protection**: Socket timeouts prevent hanging connections

## 🌟 Cool Implementation Details

### Custom URL Decoder
```python
def url_decode(s):
    # Handles %20 spaces and special characters
    # Character-by-character parsing
    # Efficient for embedded systems
```

### Smart Message Expiry
```python
def cleanup_old_messages():
    # Filters messages by timestamp
    # O(n) complexity with list comprehension
    # Runs on-demand, not continuously
```

### Session Management
```python
# Tracks users by IP address
active_users = {}  # {ip: username}
# No cookies needed!
```

## 📈 Future Enhancements

- [ ] Emoji support with picker
- [ ] Typing indicators
- [ ] Message reactions
- [ ] Private messaging
- [ ] Chat rooms/channels
- [ ] Image link previews
- [ ] Sound notifications
- [ ] Dark mode toggle

## 🎓 What I Learned

- CircuitPython socket programming
- HTTP protocol implementation from scratch
- Embedded systems resource management
- Real-time web applications without WebSockets
- Memory-efficient data structures
- Browser refresh strategies
- DaisyUI component library

## 💡 Why This is Awesome

This project demonstrates that you can build sophisticated web applications on tiny microcontrollers! No need for:
- ❌ Cloud servers
- ❌ Database systems
- ❌ Complex frameworks
- ❌ Expensive hosting

Just a $10 ESP32 chip doing all the heavy lifting! 🎉

## 📝 Code Statistics

- **Total Lines**: ~350 lines of Python
- **Functions**: 8 custom functions
- **HTML Templates**: 2 (login + chat)
- **CSS Framework**: DaisyUI + Tailwind
- **JavaScript**: ~30 lines (refresh logic)



---

Made with ❤️ and an ESP32 | No servers harmed in the making of this chat app

**Star this if you think microcontrollers are cool!** ⭐
