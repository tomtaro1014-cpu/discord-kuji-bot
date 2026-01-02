import discord
from discord import app_commands
import random
import os
import json

DATA_FILE = "roles.json"

# ---- データ読み込み ----
def load_roles():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# ---- データ保存 ----
def save_roles(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

roles = load_roles()

# ---- Bot設定 ----
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    await tree.sync()
    print(f"ログイン完了: {client.user}")

# ---- 役職指定キャラくじ ----
@tree.command(name="rolekuji", description="役職を指定してキャラくじを引く")
@app_commands.describe(role="役職名を入力")
async def rolekuji(interaction: discord.Interaction, role: str):
    if role not in roles or not roles[role]:
        await interaction.response.send_message("その役職にキャラがいないよ")
        return

    character = random.choice(roles[role])
    await interaction.response.send_message(
        f"🎯 **{role}** から選ばれたキャラは…\n👉 **{character}**！"
    )

# ---- 全キャラくじ ----
@tree.command(name="character", description="全キャラクターからランダムで1人選ぶ")
async def character(interaction: discord.Interaction):
    all_characters = []
    for char_list in roles.values():
        all_characters.extend(char_list)

    selected = random.choice(all_characters)
    await interaction.response.send_message(
        f"🎲 全キャラくじの結果は…\n👉 **{selected}**！"
    )

# ---- 役職くじ ----
@tree.command(name="role_only", description="役職だけをランダムで選ぶ")
async def role_only(interaction: discord.Interaction):
    role = random.choice(list(roles.keys()))
    await interaction.response.send_message(
        f"🧩 役職くじの結果は…\n👉 **{role}**！"
    )

# ---- キャラ追加（保存される）----
@tree.command(name="add_character", description="指定した役職にキャラクターを追加する")
@app_commands.describe(role="役職名", name="キャラクター名")
async def add_character(interaction: discord.Interaction, role: str, name: str):
    if role not in roles:
        await interaction.response.send_message("その役職は存在しないよ", ephemeral=True)
        return

    roles[role].append(name)
    save_roles(roles)

    await interaction.response.send_message(
        f"✅ **{role}** に **{name}** を追加したよ！（保存済み）"
    )

# ---- 起動 ----
client.run(os.environ["DISCORD_TOKEN"])
