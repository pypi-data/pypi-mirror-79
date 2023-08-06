from .bot import Bot

SCREEN_SIZE = (10, 10)
BACK = '⬛'
TICK = 1.1
MIN_TICK = 0.1
TIMEOUT = 30.0
PREFIX = '!'


class Game:
    def __init__(self, name: str, **kwargs):
        self.name = name
        self.prefix = kwargs.get('prefix', PREFIX)
        self.cogs = tuple(kwargs.get('cogs', ()))
        self.aliases = list(kwargs.get('aliases', []))
        self.controls = list(kwargs.get('controls', []))

        self.screen_size = tuple(kwargs.get('screen_size', SCREEN_SIZE))[:2]
        self.background = str(kwargs.get('back', BACK))
        self.title = str(kwargs.get('title', ''))
        self.footer = str(kwargs.get('footer', ''))
        self.need_input = float(kwargs.get('need_input', True))
        self.auto_clear = float(kwargs.get('auto_clear', False))

        # Ensures rate limit won't be reached if isn't solely based on input
        self.tick = max(float(kwargs.get('tick', TICK)), MIN_TICK if self.need_input else TICK)
        self.timeout = float(kwargs.get('timeout', TIMEOUT))
        self.bot_class = kwargs.get('cls', Bot)
        self.vars = kwargs.get('vars')
        self.option = kwargs

        self.input = []
        self.over = True
        self.bot = self.bot_class(self, name=self.name, prefix=self.prefix)

    @property
    def params(self):
        return self.bot.params

    @property
    def width(self):
        return self.screen_size[0]

    @property
    def height(self):
        return self.screen_size[1]

    def run(self, token: str):
        self.bot.run(token)

    def set_pregame(self):
        def decorator(func):
            self.pregame = func

        return decorator

    async def pregame(self):
        pass

    def set_update(self):
        def decorator(func):
            self.update = func

        return decorator

    async def update(self):
        raise NotImplementedError

    def set_draw(self):
        def decorator(func):
            self.draw = func

        return decorator

    async def draw(self, screen: list):
        raise NotImplementedError

    def set_postgame(self):
        def decorator(func):
            self.postgame = func

        return decorator

    async def postgame(self):
        pass

    def fill_screen(self, screen: list):
        for i in range(len(screen)):
            for j in range(len(screen[0])):
                screen[i][j] = self.background

    async def get_input(self, prompt: str, timeout: int = 0):
        if timeout > 0:
            return await self.bot.get_input(self.bot.context, prompt, timeout)
        else:
            return await self.bot.get_input(self.bot.context, prompt)

    async def change_controls(self, controls: list):
        await self.bot.add_reactions(controls)

    def quit(self):
        self.over = True
