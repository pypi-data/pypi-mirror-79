import asyncio
import discord
from discord.ext import commands
import logging
import typing
import time

TIMEOUT = 15.0
DELETE = 10.0
COOLDOWN = 30.0


class Bot(commands.Bot):
    def __init__(self, game, name: str, prefix: str):
        super().__init__(command_prefix=prefix, allowed_mentions=discord.AllowedMentions(everyone=False))

        self.add_command(commands.Command(self.game_command, name=name, aliases=game.aliases))
        self.context = None
        self.message = None
        self.reactions = None
        self.params = ''
        self.cooldown = 0.0
        self.timer = 0.0
        self.game = game
        self.name = name

    async def on_ready(self):
        cogs = self.game.cogs
        for cog in cogs:
            try:
                self.load_extension(cog)
            except commands.ExtensionAlreadyLoaded:
                logging.warning(f'{cog} has already been loaded.')

        await self.change_presence(activity=discord.Game(name=f'{self.game.prefix}{self.name}'),
                                   status=discord.Status.online)
        logging.info('Ready to play!')

    async def on_message(self, message: discord.Message):
        ctx = await self.get_context(message, cls=BotContext)
        if ctx.command and ctx.command.name == self.name:
            if self.game.over:
                await self.invoke(ctx)
            elif time.time() > self.cooldown:
                await ctx.send(f'{self.context.author.name} is playing right now!')
                self.cooldown = time.time() + COOLDOWN
        else:
            await self.invoke(ctx)

    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        try:
            if str(reaction.emoji) in self.reactions and user.id == self.context.author.id and not user.bot and \
                    reaction.message.id == self.message.id:
                self.game.input.insert(0, reaction.emoji)
                self.timer = time.time()

                if self.game.auto_clear:
                    await self.message.remove_reaction(reaction.emoji, user)
        except (AttributeError, TypeError):
            logging.info('No context or reactions currently.')

    async def on_reaction_remove(self, reaction: discord.Reaction, user: discord.User):
        if not self.game.auto_clear:
            try:
                if str(reaction.emoji) in self.reactions and user.id == self.context.author.id and not user.bot and \
                        reaction.message.id == self.message.id:
                    self.game.input.insert(0, reaction.emoji)
                    self.timer = time.time()
            except (AttributeError, TypeError):
                logging.info('No context or reactions currently.')

    async def on_command_error(self, ctx: commands.Context, exception: discord.DiscordException):
        if not isinstance(exception, commands.CommandNotFound):
            raise exception

    async def game_command(self, ctx: commands.Context, *, params: typing.Optional[str]):
        screen = [[self.game.background] * self.game.height for _ in range(self.game.width)]
        self.game.over = False
        await asyncio.sleep(0.25)

        self.context = ctx
        self.params = params

        await self.game.pregame()
        await self.game.draw(screen)
        self.message = await ctx.send(self.make_screen(screen))
        await self.add_reactions(self.game.controls)
        await asyncio.sleep(self.game.tick)

        tick = time.time()
        self.timer = time.time()
        while True:
            if not self.game.need_input or self.game.input:
                await self.game.update()
                await self.game.draw(screen)
                self.game.input = []

                await self.message.edit(content=self.make_screen(screen))

            if self.game.over or time.time() - self.timer > self.game.timeout:
                break
            await asyncio.sleep(max(self.game.tick - (time.time() - tick), 0.0))
            tick = time.time()

        await asyncio.sleep(0.25)
        await self.game.postgame()
        await self.message.clear_reactions()

        self.game.over = True
        self.context = None
        self.message = None
        self.params = ''

    async def add_reactions(self, reactions: list):
        self.reactions = reactions

        await self.message.clear_reactions()
        for react in self.reactions:
            await asyncio.sleep(0.25)
            await self.message.add_reaction(react)

    def make_screen(self, screen: list):
        output = ''
        for i in range(len(screen[0])):
            output += ''.join([row[i] for row in screen]) + '\n'
        return f'{self.game.title}\n{output}{self.game.footer}'

    async def get_input(self, ctx: commands.Context, text: str = '', timeout: float = TIMEOUT):
        def check(msg: discord.Message):
            return msg.author == ctx.author and msg.channel == ctx.channel

        message = await ctx.send(text if text else 'Input:')
        try:
            response = await ctx.bot.wait_for('message', check=check, timeout=timeout)
            content = response.clean_content

            await response.delete()
            await message.delete()
            return content
        except asyncio.TimeoutError:
            await message.edit(content='Timed out!', delete_after=DELETE)
            return ''


class BotContext(commands.Context):
    @property
    def game(self):
        return self.bot.game

