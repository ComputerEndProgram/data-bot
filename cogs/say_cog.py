import discord
from discord.ext import commands

class SayCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="say", description="Make the bot say something in a channel")
    async def say(self, ctx, channel: discord.TextChannel, message: str):
        if not ctx.author.guild_permissions.administrator:
            await ctx.respond("You don't have permission to use this command.", ephemeral=True)
            return
        await channel.send(message)
        await ctx.respond("Message sent!", ephemeral=True)

def setup(bot):
    bot.add_cog(SayCog(bot))
