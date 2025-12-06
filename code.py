import wifi
import socketpool
import time
import os

# -------------------------------
# Wi-Fi
# -------------------------------
wifi.radio.connect(
    os.getenv("CIRCUITPY_WIFI_SSID"),
    os.getenv("CIRCUITPY_WIFI_PASSWORD")
)
ip = wifi.radio.ipv4_address
print("Connected, IP:", ip)

pool = socketpool.SocketPool(wifi.radio)

try:
    server = pool.socket()
    server.setsockopt(pool.SOL_SOCKET, pool.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", 80))
    server.listen(5)
    print("Server bound to port 80")
except OSError as e:
    print(f"Socket error: {e}")
    time.sleep(3)
    import microcontroller
    microcontroller.reset()

# -------------------------------
# Message Storage
# -------------------------------
messages = []
MESSAGE_TTL = 20
MAX_USERS = 5
active_users = {}

def cleanup_old_messages():
    current_time = time.monotonic()
    global messages
    messages[:] = [(u, msg, ts) for u, msg, ts in messages if current_time - ts < MESSAGE_TTL]

def add_message(user, text):
    messages.append((user, text, time.monotonic()))
    if len(messages) > 20:
        messages.pop(0)

def get_username(ip):
    return active_users.get(ip)

def set_username(ip, username):
    if ip not in active_users and len(active_users) >= MAX_USERS:
        return False
    active_users[ip] = username[:20]
    return True

# -------------------------------
# URL Decoder
# -------------------------------
def url_decode(s):
    s = s.replace("+", " ")
    i = 0
    result = []
    while i < len(s):
        if s[i] == '%' and i + 2 < len(s):
            try:
                result.append(chr(int(s[i+1:i+3], 16)))
                i += 3
            except:
                result.append(s[i])
                i += 1
        else:
            result.append(s[i])
            i += 1
    return ''.join(result)

# -------------------------------
# Login Page
# -------------------------------
def login_page():
    user_count = len(active_users)
    status = f"{user_count}/{MAX_USERS} users online" if user_count > 0 else "No users online"
    warning = '<div class="alert alert-error mt-4"><span>Chat is full! Please try again later.</span></div>' if user_count >= MAX_USERS else ''
    
    return f"""HTTP/1.1 200 OK
Content-Type: text/html
Connection: close

<!DOCTYPE html>
<html data-theme="cupcake">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Login - ESP32 Chat</title>
<link href="https://cdn.jsdelivr.net/npm/daisyui@4.12.14/dist/full.min.css" rel="stylesheet">
<script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="min-h-screen bg-gradient-to-br from-primary to-secondary flex items-center justify-center p-4">
<div class="card w-full max-w-md bg-base-100 shadow-2xl">
<div class="card-body">
<div class="text-center mb-4">
<h1 class="text-4xl font-bold mb-2">ð¬ ESP32 Chat</h1>
<div class="badge badge-primary badge-lg">{status}</div>
</div>
<form class="space-y-4">
<div class="form-control">
<label class="label">
<span class="label-text font-semibold">Your Name</span>
</label>
<input type="text" name="username" placeholder="Enter your name" maxlength="20" required autofocus
class="input input-bordered input-primary w-full">
</div>
<button type="submit" class="btn btn-primary w-full btn-lg">
Join Chat
</button>
</form>
{warning}
</div>
</div>
</body>
</html>
"""

# -------------------------------
# Chat Page
# -------------------------------
def chat_page(user):
    cleanup_old_messages()
    
    chat = []
    for u, msg, _ in messages:
        if u == user:
            chat.append(f'<div class="chat chat-end"><div class="chat-header">{u}</div><div class="chat-bubble chat-bubble-primary">{msg}</div></div>')
        else:
            chat.append(f'<div class="chat chat-start"><div class="chat-header">{u}</div><div class="chat-bubble chat-bubble-secondary">{msg}</div></div>')
    
    chat_html = ''.join(chat) if chat else '<div class="text-center text-base-content/50 mt-8 text-lg">No messages yet. Start the conversation!</div>'
    user_list = ", ".join(active_users.values())
    
    return f"""HTTP/1.1 200 OK
Content-Type: text/html
Connection: close

<!DOCTYPE html>
<html data-theme="cupcake">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Chat - {user}</title>
<link href="https://cdn.jsdelivr.net/npm/daisyui@4.12.14/dist/full.min.css" rel="stylesheet">
<script src="https://cdn.tailwindcss.com"></script>
<script>
var isTyping = false;
var refreshTimer = null;

function startRefresh() {{
  refreshTimer = setInterval(function() {{
    if (!isTyping) {{
      location.reload();
    }}
  }}, 3000);
}}

window.onload = function() {{
  var msgInput = document.getElementById('msgInput');
  var messages = document.getElementById('messages');
  
  messages.scrollTop = messages.scrollHeight;
  
  msgInput.addEventListener('focus', function() {{
    isTyping = true;
  }});
  
  msgInput.addEventListener('blur', function() {{
    setTimeout(function() {{
      isTyping = false;
    }}, 500);
  }});
  
  msgInput.addEventListener('input', function() {{
    isTyping = true;
  }});
  
  startRefresh();
}};
</script>
</head>
<body class="bg-base-200">
<div class="navbar bg-primary text-primary-content shadow-lg">
<div class="flex-1">
<a class="btn btn-ghost text-xl">ð¬ ESP32 Chat</a>
</div>
<div class="flex-none">
<div class="dropdown dropdown-end">
<label tabindex="0" class="btn btn-ghost btn-circle">
<div class="indicator">
<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" /></svg>
<span class="badge badge-sm indicator-item">{len(active_users)}</span>
</div>
</label>
<ul tabindex="0" class="menu menu-sm dropdown-content mt-3 z-[1] p-2 shadow bg-base-100 rounded-box w-52">
<li class="menu-title">Online Users</li>
<li><a>{user_list}</a></li>
</ul>
</div>
</div>
</div>

<div class="container mx-auto max-w-4xl p-4">
<div class="card bg-base-100 shadow-xl" style="height:calc(100vh - 180px)">
<div class="card-body p-4">
<div id="messages" class="overflow-y-auto h-full space-y-2">
{chat_html}
</div>
</div>
</div>

<div class="card bg-base-100 shadow-xl mt-4">
<div class="card-body p-4">
<div class="flex gap-2">
<form class="flex-1 flex gap-2">
<input type="text" id="msgInput" name="msg" placeholder="Type your message..." required
class="input input-bordered input-primary flex-1">
<button type="submit" class="btn btn-primary">
<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" /></svg>
Send
</button>
</form>
<form action="/?logout=1">
<button class="btn btn-error btn-outline">Exit</button>
</form>
</div>
</div>
</div>
</div>
</body>
</html>
"""

# -------------------------------
# Server Loop
# -------------------------------
print(f"Chat server: http://{ip}")

buffer = bytearray(1024)

while True:
    conn = None
    try:
        conn, addr = server.accept()
        conn.settimeout(3.0)
        
        client_ip = str(addr[0])
        bytes_received = conn.recv_into(buffer)
        
        if bytes_received > 0:
            request = str(buffer[:bytes_received], "utf-8", "ignore")
            
            username = get_username(client_ip)
            
            if "logout=1" in request:
                if client_ip in active_users:
                    print(f"User left: {active_users[client_ip]}")
                    del active_users[client_ip]
                conn.send(login_page().encode("utf-8"))
                continue
            
            if not username and "username=" in request:
                try:
                    start = request.index("username=") + 9
                    end = request.index("&", start) if "&" in request[start:] else request.index(" ", start)
                    new_username = url_decode(request[start:end]).strip()
                    
                    if new_username and len(new_username) > 0:
                        if set_username(client_ip, new_username):
                            username = new_username
                            print(f"User joined: {username}")
                        else:
                            conn.send(login_page().encode("utf-8"))
                            continue
                except:
                    pass
            
            if not username:
                conn.send(login_page().encode("utf-8"))
                continue
            
            if "GET /?" in request and "msg=" in request:
                try:
                    start = request.index("msg=") + 4
                    end = request.index("&", start) if "&" in request[start:] else request.index(" ", start)
                    msg = url_decode(request[start:end]).strip()
                    
                    if msg:
                        add_message(username, msg)
                        print(f"{username}: {msg}")
                except:
                    pass
            
            conn.send(chat_page(username).encode("utf-8"))
        
    except OSError as e:
        if e.errno != 116:
            print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass