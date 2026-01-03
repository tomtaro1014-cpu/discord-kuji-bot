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
intents = discord.Intents.default
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    await tree.sync()
    print(f"ログイン完了: {client.user}")

# ---- 役職指定キャラくじ ----
@tree.command(name="role_herokuji", description="ロールを指定してヒーローくじを引く")
@app_commands.describe(role="ロール名を入力")
async def rolekuji(interaction: discord.Interaction, role: str):
    if role not in roles or not roles[role]:
        await interaction.response.send_message("そのロールにヒーローがいないよ")
        return

    character = random.choice(roles[role])
    await interaction.response.send_message(
        f"🎯 **{role}** から選ばれたヒーローは…\n👉 **{character}**！"
    )

# ---- 全キャラくじ ----
@tree.command(name="herokuji", description="全ヒーローからランダムで1人選ぶ")
async def character(interaction: discord.Interaction):
    all_characters = []
    for char_list in roles.values():
        all_characters.extend(char_list)

    selected = random.choice(all_characters)
    await interaction.response.send_message(
        f"🎲 全ヒーローくじの結果は…\n👉 **{selected}**！"
    )

# ---- 役職くじ ----
@tree.command(name="rolekuji", description="ロールだけをランダムで選ぶ")
async def role_only(interaction: discord.Interaction):
    role = random.choice(list(roles.keys()))
    await interaction.response.send_message(
        f"🧩 ロールくじの結果は…\n👉 **{role}**！"
    )

# ---- キャラ追加（保存される）----
@tree.command(name="add_hero", description="指定したロールにヒーローを追加する")
@app_commands.describe(role="ロール名", name="ヒーロー名")
async def add_hero(interaction: discord.Interaction, role: str, name: str):
    if role not in roles:
        await interaction.response.send_message("そのロールは存在しないよ", ephemeral=True)
        return

    roles[role].append(name)
    save_roles(roles)

    await interaction.response.send_message(
        f"✅ **{role}** に **{name}** を追加したよ！（保存済み）"
    )

# ---- 起動 ----
client.run(os.environ["DISCORD_TOKEN"])
