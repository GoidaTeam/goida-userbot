import os
import json
import time
import subprocess
from pyrogram.enums import ParseMode

try:
    import psutil
    HAS_PSUTIL = True
except:
    HAS_PSUTIL = False

# URL для превью (используйте Telegraph статью или страницу с og:image)
# Для правильного превью нужен URL страницы, а не прямой ссылки на изображение
IMAGE_URL = "https://te.legra.ph/Forelka-Userbot-01-05"

async def info_cmd(client, message, args):
    """Информация о юзерботе"""
    
    # Получаем информацию о владельце
    me = client.me
    owner_name = f"{me.first_name or ''} {me.last_name or ''}".strip()
    if not owner_name:
        owner_name = "Unknown"
    
    # Получаем текущий префикс
    path = f"config-{me.id}.json"
    prefix = "."
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                cfg = json.load(f)
                prefix = cfg.get("prefix", ".")
        except:
            pass
    
    # Получаем текущую ветку git
    try:
        branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            stderr=subprocess.DEVNULL
        ).decode().strip()
    except:
        branch = "unknown"
    
    # Считаем uptime
    start_time = getattr(client, 'start_time', time.time())
    uptime_seconds = int(time.time() - start_time)
    days, remainder = divmod(uptime_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    uptime_parts = []
    if days > 0:
        uptime_parts.append(f"{days}д")
    if hours > 0:
        uptime_parts.append(f"{hours}ч")
    if minutes > 0:
        uptime_parts.append(f"{minutes}м")
    uptime_parts.append(f"{seconds}с")
    uptime_str = " ".join(uptime_parts)
    
    # Получаем использование RAM текущим процессом
    if HAS_PSUTIL:
        try:
            process = psutil.Process()
            ram_usage_bytes = process.memory_info().rss
            ram_usage_mb = ram_usage_bytes / (1024 * 1024)
            ram_usage_str = f"{ram_usage_mb:.1f} MB"
        except:
            ram_usage_str = "N/A"
    else:
        ram_usage_str = "N/A"
    
    # Получаем имя хоста
    try:
        hostname = subprocess.check_output(["hostname"]).decode().strip()
    except:
        hostname = os.uname().nodename if hasattr(os, 'uname') else "Unknown"
    
    # Формируем текст с невидимой ссылкой для превью
    # Добавляем URL в конец через zero-width space для генерации preview
    text = f"""<blockquote><emoji id=5461117441612462242>🔥</emoji> Forelka Userbot</blockquote>

<blockquote><emoji id=5879770735999717115>👤</emoji> Владелец: {owner_name}</blockquote>

<blockquote><emoji id=5778423822940114949>🌿</emoji> Branch: {branch}</blockquote>

<blockquote><emoji id=5877396173135811032>⚙️</emoji> Prefix: «{prefix}»
<emoji id=5778550614669660455>⏱</emoji> Uptime: {uptime_str}</blockquote>

<blockquote><emoji id=5936130851635990622>💾</emoji> RAM usage: {ram_usage_str}
<emoji id=5870982283724328568>🖥</emoji> Host: {hostname}</blockquote>

<a href="{IMAGE_URL}">&#8205;</a>"""
    
    # Удаляем исходное сообщение и отправляем новое с превью
    await message.delete()
    await client.send_message(
        chat_id=message.chat.id,
        text=text,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=False
    )

def register(app, commands, module_name):
    """Регистрация команды"""
    commands["info"] = {"func": info_cmd, "module": module_name}
