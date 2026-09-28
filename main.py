import os
import random
import threading
from datetime import datetime
import pytz
from flask import Flask
import discord
from discord.ext import tasks, commands

# --- สร้าง Web Server เพื่อให้ Render ทำงานได้ตลอดเวลา ไม่ดับ ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = threading.Thread(target=run_web)
    t.start()

# --- Discord Self-Bot Setup ---
client = commands.Bot(command_prefix="!", self_bot=True)

# ⚠️ นำลิงก์รูปภาพปกสตรีมที่คุณฝากรูปไว้มาใส่ตรงนี้ (เช่น Imgur หรือ Discord CDN)
IMAGE_URL = "https://i.imgur.com/d6864a2bf8a5568f8f616fbf116c7a81.jpg"

@client.event
async def on_ready():
    print(f"ล็อกอินสำเร็จในชื่อ: {client.user}")
    change_status.start()

@tasks.loop(seconds=30)  # อัปเดตเวลาและปิงทุกๆ 30 วินาที
async def change_status():
    # ดึงเวลาปัจจุบัน (โซนประเทศไทย)
    tz = pytz.timezone('Asia/Bangkok')
    now = datetime.now(tz)
    
    # แปลงชื่อวันเป็นภาษาไทย
    days_th = ["วันจันทร์", "วันอังคาร", "วันพุธ", "วันพฤหัสบดี", "วันศุกร์", "วันเสาร์", "วันอาทิตย์"]
    day_str = days_th[now.weekday()]
    time_str = now.strftime("%H:%M")
    
    # สุ่มค่า Ping (ให้ใกล้เคียงกัน เช่น 24-29) และ องศา (20-23)
    ping_val = random.randint(24, 29)
    temp_val = random.randint(20, 23)
    
    # จัดรูปแบบบรรทัดตามที่ต้องการ
    line1 = "Valan... 𓇼 ⋆.˚ 𓆉 𓆝 𓆡⋆.˚ 𓇼"
    line2 = f"{day_str} {time_str}𓋜"
    line3 = f"Ping {ping_val}ms {temp_val}°C ၄၃"
    
    # สร้างสถานะสตรีมมิ่ง
    activity = discord.Streaming(
        name=line1,
        details=line2,
        state=line3,
        url="https://www.twitch.tv/discord",  # URL สำหรับเปิดโหมดสตรีมสีม่วง
        assets={
            "large_image": IMAGE_URL,
            "large_text": "Valan Status"
        }
    )
    
    await client.change_presence(activity=activity)

if __name__ == "__main__":
    keep_alive()  # เริ่มทำงาน Web Server
    
    # ดึง Token จาก Environment Variables บน Render
    token = os.getenv("TOKEN")
    if token:
        client.run(token)
    else:
        print("ERROR: ไม่พบ TOKEN ใน Environment Variables!")
