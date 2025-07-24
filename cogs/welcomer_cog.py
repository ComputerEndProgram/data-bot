import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import aiohttp
import io
import os

class WelcomerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = {
            "welcome_channel_id": None,
            "welcome_dm": "Welcome to {server}, {user}!",
            "welcome_image": "welcome_template.png",
            "welcome_font": "OpenSans-Bold.ttf"
        }

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # --- Dynamic Welcome Image ---
        try:
            base = Image.open(self.config["welcome_image"]).convert("RGBA")
            draw = ImageDraw.Draw(base)
            font = ImageFont.truetype(self.config["welcome_font"], 48)

            username = member.display_name
            text = f"Welcome, {username}!"
            # Center text at bottom of image
            text_w, text_h = draw.textsize(text, font=font)
            x = (base.width - text_w) // 2
            y = base.height - text_h - 50
            draw.text((x, y), text, font=font, fill="white")

            # Fetch and paste avatar
            async with aiohttp.ClientSession() as session:
                async with session.get(str(member.avatar.url)) as resp:
                    avatar_bytes = await resp.read()
            avatar_img = Image.open(io.BytesIO(avatar_bytes)).resize((128, 128)).convert("RGBA")
            base.paste(avatar_img, (20, 20), avatar_img)

            buffer = io.BytesIO()
            base.save(buffer, "PNG")
            buffer.seek(0)

            # Send to welcome channel
            channel = None
            if self.config["welcome_channel_id"]:
                channel = member.guild.get_channel(self.config["welcome_channel_id"])
            if channel:
                await channel.send(file=discord.File(fp=buffer, filename="welcome.png"))
        except Exception as e:
            print(f"Welcome image error: {e}")

        # --- Send Welcome DM ---
        try:
            dm_text = self.config["welcome_dm"].replace("{user}", member.mention).replace("{server}", member.guild.name)
            await member.send(dm_text)
        except Exception as e:
            print(f"Welcome DM error: {e}")

    @commands.slash_command(name="setwelcomechannel", description="Set the channel for welcome images")
    async def setwelcomechannel(self, ctx, channel: discord.TextChannel):
        self.config["welcome_channel_id"] = channel.id
        await ctx.respond(f"Welcome channel set to {channel.mention}", ephemeral=True)

    @commands.slash_command(name="setwelcomemsg", description="Set the DM message for new members")
    async def setwelcomemsg(self, ctx, *, message: str):
        self.config["welcome_dm"] = message
        await ctx.respond("Welcome DM message updated.", ephemeral=True)

    @commands.slash_command(name="setwelcomeimage", description="Set the image file for welcome messages")
    async def setwelcomeimage(self, ctx, *, filename: str):
        if os.path.exists(filename):
            self.config["welcome_image"] = filename
            await ctx.respond(f"Welcome image set to `{filename}`.", ephemeral=True)
        else:
            await ctx.respond("File not found.", ephemeral=True)

    @commands.slash_command(name="setwelcomefont", description="Set the font file for welcome images")
    async def setwelcomefont(self, ctx, *, filename: str):
        if os.path.exists(filename):
            self.config["welcome_font"] = filename
            await ctx.respond(f"Welcome font set to `{filename}`.", ephemeral=True)
        else:
            await ctx.respond("File not found.", ephemeral=True)

def setup(bot):
    bot.add_cog(WelcomerCog(bot))
