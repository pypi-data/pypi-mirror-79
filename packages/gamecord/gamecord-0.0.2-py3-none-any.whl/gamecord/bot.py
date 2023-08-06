import asyncio
import discord
from discord.ext import commands
import logging
import time


class Bot(commands.Bot):
    def __init__(self, game, name: str, prefix: str):
        super().__init__(command_prefix=prefix, allowed_mentions=discord.AllowedMentions(everyone=False))

        self.add_command(commands.Command(self.game_command, name=name, aliases=game.aliases))
        self.context = None
        self.message = None
        self.reactions = None
        self.game = game
        self.name = name

    async def on_ready(self):
        await self.change_presence(activity=discord.Game(name=f'{self.game.prefix}{self.name}'),
                                   status=discord.Status.online)
        logging.info('Ready for tagging!')

    async def on_message(self, message: discord.Message):
        if self.game.over:
            await self.process_commands(message)

    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        if user.id == self.context.author.id and reaction.message.id == self.message.id and \
                str(reaction.emoji) in self.reactions:
            self.game.input.insert(0, reaction.emoji)
            await self.message.remove_reaction(reaction.emoji, user)

    async def on_command_error(self, ctx: commands.Context, exception: discord.DiscordException):
        if not isinstance(exception, commands.CommandNotFound):
            logging.warning(exception)

    async def game_command(self, ctx: commands.Context):
        screen = [[self.game.background] * self.game.screen_size[1] for _ in range(self.game.screen_size[0])]

        self.context = ctx
        self.message = await ctx.send(self.make_screen(screen))
        await self.add_reactions(self.game.controls)

        tick = time.time()
        self.game.over = False
        self.game.draw(screen)
        await self.message.edit(content=self.make_screen(screen))

        while True:
            if not self.game.need_input or self.game.input:
                self.game.update()
                self.game.draw(screen)
                self.game.input = []

                await self.message.edit(content=self.make_screen(screen))

            if self.game.over:
                break
            await asyncio.sleep(max(self.game.tick - (time.time() - tick), 0.0))
            tick = time.time()
        await asyncio.sleep(0.25)
        await self.message.clear_reactions()
        self.context = None
        self.message = None

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
        return f'{self.game.title}\n{output}\n{self.game.footer}'
