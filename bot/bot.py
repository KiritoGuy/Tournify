from pathlib import Path

import discord
from config import BOT_TOKEN # config file
from discord.errors import Forbidden
from discord.ext import commands
from discord.ext.commands import CommandNotFound, Context

IGNORE_EXCEPTIONS = (CommandNotFound,)

"""	
Setup bot intents (events restrictions)
For more information about intents, please go to the following websites:
https://discordpy.readthedocs.io/en/latest/intents.html
https://discordpy.readthedocs.io/en/latest/intents.html#privileged-intents
Default Intents:
intents.bans = True
intents.dm_messages = True
intents.dm_reactions = True
intents.dm_typing = True
intents.emojis = True
intents.emojis_and_stickers = True
intents.guild_messages = True
intents.guild_reactions = True
intents.guild_scheduled_events = True
intents.guild_typing = True
intents.guilds = True
intents.integrations = True
intents.invites = True
intents.messages = True # `message_content` is required to get the content of the messages
intents.reactions = True
intents.typing = True
intents.voice_states = True
intents.webhooks = True
Privileged Intents (Needs to be enabled on developer portal of Discord), please use them only if you need them:
intents.members = True
intents.message_content = True
intents.presences = True
"""

intents = discord.Intents.default()

intents.members = True # you can add your seperate intents as per required
intents.message_content = True
intents.presences = True


class Tournify(commands.Bot):
    def __init__(self):
        self.ready = False
        self._cogs = [p.stem for p in Path(".").glob("./bot/cogs/*.py")]
        super().__init__(
            command_prefix=self.prefix,
            case_insensitive=True,
            intents=intents,
            help_command=None)

    def setup(self):
        print("Running setup...")
        print("--------------------------")
        for cog in self._cogs:
            try:
                self.load_extension(f"bot.cogs.{cog}")
                print(f"Loaded cog {cog}.")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                print(f"Failed to load extension {extension}\n\n{exception}")
        print("--------------------------")
        print("Setup complete.")

    def run(self):
        self.setup()

        print("Running bot....")
        super().run(BOT_TOKEN, reconnect=True)

    async def shutdown(self):
        print("Shutting down.")
        await super().close()

    async def close(self):
        print("Closing...")
        await self.shutdown()

    async def on_connect(self):
        print("bot connected.")

    async def on_resumed(self):
        print("bot resumed.")

    async def on_disconnect(self):
        print("bot disconnected.")

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Something went wrong.")
        raise

    async def on_command_error(self, ctx, exc):
        if any([isinstance(exc, error) for error in IGNORE_EXCEPTIONS]):
            pass

        elif hasattr(exc, "original"):
            # if isinstance(exc.original, HTTPException):
            # 	await ctx.send("Unable to send message.")

            if isinstance(exc.original, Forbidden):
                await ctx.send("I do not have permission to do that.")

            else:
                raise exc.original

        else:
            raise exc

    async def on_ready(self):
        self.ready = True
        print("TOURNIFY IS READY.")
        statuses = ["WITH YOU!", "TERKENAL ARMY!", "ALL GAMES!"]
        await self.Tournify.change_presence(activity=discord.Game(random.choice(statuses)))


    async def prefix(self, bot, msg):
        return commands.when_mentioned_or("!")(bot, msg)

    async def process_commands(self, message):
        ctx = await self.get_context(message, cls=Context)

        if ctx.command is not None and ctx.guild is not None:
            if not self.ready:
                await ctx.send("I'm not ready to receive commands. Please wait a few seconds.")

            else:
                await self.invoke(ctx)

    async def on_message(self, message):
        if not message.author.bot:
            await self.process_commands(message)
