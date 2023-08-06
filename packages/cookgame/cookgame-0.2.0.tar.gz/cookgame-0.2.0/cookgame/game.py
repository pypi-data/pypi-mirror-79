import arcade
import random
import math
import os
MUSIC_VOLUME = 0.05
DUSTBIN_SCALE = 0.7
RUBBISH_SCALE = 0.2
CHANGE_RATE_X = 7.2
CHANGE_RATE_Y = 12.38
SOUNDPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sound/')

TEXTUREPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           'textures/')
print(SOUNDPATH, TEXTUREPATH)
ALL = [
    'apple.png', 'banana.png', 'bone.png', 'bottle.png', 'chick.png',
    'cola.png', 'fish.png'
]


class Rubbish(arcade.Sprite):
    '''
    垃圾实体类
    '''
    def __init__(self, name, s=0.5):
        super().__init__(name, scale=s)
        self.change_rate_x = CHANGE_RATE_X
        self.change_rate_y = CHANGE_RATE_Y

    def set_change_rate(self, x=CHANGE_RATE_X, y=CHANGE_RATE_Y):
        self.change_rate_x = x
        self.change_rate_y = y

    def set_xy(self, x, y, angle=0, changeangle=1, dir=0):
        self.center_x = x
        self.center_y = y
        self.angle = angle
        self.change_angle = changeangle
        self.direction = dir

    def update_xy(self):
        self.change_x = self.change_rate_x * math.cos(math.radians(self.angle))
        self.change_y = self.change_rate_y * math.sin(math.radians(self.angle))


class Dustbin(arcade.Sprite):
    '''
    垃圾桶实体类
    '''
    def __init__(self, t=1, s=0.5):
        super().__init__()

        self.open_textures = [
            arcade.load_texture(TEXTUREPATH + 'blue_open.png'),
            arcade.load_texture(TEXTUREPATH + 'red_open.png'),
            arcade.load_texture(TEXTUREPATH + 'yellow_open.png'),
            arcade.load_texture(TEXTUREPATH + 'green_open.png'),
            arcade.load_texture(TEXTUREPATH + 'grey_open.png')
        ]
        self.close_textures = [
            arcade.load_texture(TEXTUREPATH + 'blue_close.png'),
            arcade.load_texture(TEXTUREPATH + 'red_close.png'),
            arcade.load_texture(TEXTUREPATH + 'yellow_close.png'),
            arcade.load_texture(TEXTUREPATH + 'green_close.png'),
            arcade.load_texture(TEXTUREPATH + 'grey_close.png')
        ]
        self.scale = s
        #垃圾桶的造型下标(传入的值时1~5)
        self.type = t - 1
        #垃圾桶的造型
        self.texture = self.close_textures[self.type]
        #垃圾桶状态 0表示关闭（默认），1表示开启
        self.state = 0

    def change(self):

        if self.state:
            self.state = 0
            self.texture = self.close_textures[self.type]
        else:
            self.state = 1
            self.texture = self.open_textures[self.type]


class Kitchen(arcade.Window):
    def __init__(self, width=400, height=600, title='GAME'):
        super().__init__(width, height, title)

    def build(self, l=4, r=2, num=1):

        self.rubbish_textures = [TEXTUREPATH + 'paper.png']
        if num > 1 and num <= len(ALL):
            self.rubbish_textures = random.sample(ALL, num)
        self.has_bomb = False
        self.allow_music = True
        self.is_music_start = False
        self.GAME_PAUSE = False
        self.frame_count = 0
        self.frames = 10
        self.end_text = '厨房炸了'
        self.end_color = arcade.color.RED
        self.end_size = 48
        self.score = 0

        self.leftkey = None
        self.rightkey = None

        self.music = arcade.Sound(SOUNDPATH + "happy.mp3")
        self.bomb = arcade.Sound(SOUNDPATH + 'bomb.wav', streaming=True)
        self.bgname = TEXTUREPATH + 'kitchen.jpg'
        self.background_image = arcade.load_texture(self.bgname)

        self.db_left = Dustbin(t=l, s=DUSTBIN_SCALE)
        self.db_left.center_x = 60
        self.db_left.center_y = 60
        self.db_right = Dustbin(t=r, s=DUSTBIN_SCALE)
        self.db_right.center_x = 340
        self.db_right.center_y = 60
        self.dustbins = arcade.SpriteList()
        self.rubbishs = arcade.SpriteList()
        self.kills = arcade.SpriteList()
        self.miscs = arcade.SpriteList()
        self.dustbins.append(self.db_left)
        self.dustbins.append(self.db_right)

    def add_vase(self, x=60, y=347):
        s = arcade.Sprite(TEXTUREPATH + 'vase.png', scale=0.4)
        s.center_x = x
        s.center_y = y
        self.miscs.append(s)

    def bomb_off(self):
        if self.has_bomb:
            self.rubbish_textures.remove(TEXTUREPATH + 'bomb.png')
            self.has_bomb = False

    def bomb_on(self):
        if not self.has_bomb:
            self.rubbish_textures.append(TEXTUREPATH + 'bomb.png')
            self.has_bomb = True

    def add_light(self, x=200, y=505):
        s = arcade.Sprite(TEXTUREPATH + 'lights.png', scale=1)
        s.center_x = x
        s.center_y = y
        self.miscs.append(s)

    def set_end(self, text, c=arcade.color.RED, s=48):
        self.end_text = text
        self.end_color = c
        self.end_size = s

    def music_off(self):
        self.allow_music = False

    def music_on(self):
        self.allow_music = True

    def set_rb(self, s):
        global RUBBISH_SCALE
        RUBBISH_SCALE = s

    def set_bg(self, bg):
        self.bgname = bg

    def add_rb(self, name):
        if name not in self.rubbish_textures:
            #前插是为了保证bomb.png必须在rubbish_textures的最后一个
            self.rubbish_textures.insert(0, TEXTUREPATH + name)

    def set_speed(self, num):
        if num >= 0:
            self.frames = num

    def check(self, dustbin, rubbishlist, score=1):
        lst = arcade.check_for_collision_with_list(dustbin, rubbishlist)

        for r in lst:
            if dustbin.state == 1:  #open
                if self.has_bomb and r.idx == len(self.rubbish_textures) - 1:
                    dustbin.texture = arcade.load_texture(TEXTUREPATH +
                                                          'explode.png')
                    r.kill()
                    self.GAME_PAUSE = True
                    self.music.stop()
                    self.bomb.play()
                else:
                    self.score += score
                    self.kills.append(r)

            else:
                r.change_rate_y *= -1
                r.change_rate_x *= 3

    def set_left(self, k):
        a = str.upper(k)
        if a in dir(arcade.key):
            self.leftkey = getattr(arcade.key, a)

    def set_right(self, k):
        a = str.upper(k)
        if a in dir(arcade.key):
            self.leftkey = getattr(arcade.key, a)

    def on_update(self, delta_time: float):

        if not self.GAME_PAUSE:

            if self.allow_music:
                if not self.is_music_start:
                    self.music.play(MUSIC_VOLUME)
                    self.is_music_start = True
                else:
                    if self.music.get_stream_position() == 0:
                        self.music.play(MUSIC_VOLUME)

            if self.frame_count >= self.frames:
                self.frame_count = 0

                if random.randint(1, 3) == 1:
                    idx = random.randrange(len(self.rubbish_textures))
                    rubbish = Rubbish(self.rubbish_textures[idx],
                                      RUBBISH_SCALE)
                    rubbish.idx = idx

                    if random.randint(0, 1):
                        rubbish.set_xy(420,
                                       random.randint(400, 550),
                                       angle=180,
                                       changeangle=-1)
                        rubbish.set_change_rate(y=-12.38)
                    else:
                        rubbish.set_xy(-20,
                                       random.randint(400, 550),
                                       changeangle=-1)

                    self.rubbishs.append(rubbish)
            else:
                self.frame_count += 1

            self.check(self.db_left, self.rubbishs)
            self.check(self.db_right, self.rubbishs)

            for r in self.rubbishs:

                r.update_xy()
                if r.right < -50 and r.direction == 1:
                    self.kills.append(r)
                if r.left > self.width + 50 and r.direction == 0:
                    self.kills.append(r)

        for k in self.kills:
            k.kill()
        self.miscs.update()
        self.dustbins.update()
        self.rubbishs.update()

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, self.width, self.height,
                                            self.background_image)

        self.miscs.draw()
        arcade.draw_text(f'得分:{self.score}',
                         20,
                         550,
                         color=arcade.color.PURPLE_NAVY,
                         font_size=30,
                         font_name='simhei')
        if self.GAME_PAUSE:
            arcade.draw_text(self.end_text,
                             200,
                             300,
                             anchor_x='center',
                             anchor_y='top',
                             align='center',
                             color=self.end_color,
                             font_size=self.end_size,
                             bold=True,
                             font_name='simhei')

        self.dustbins.draw()
        self.rubbishs.draw()

    def on_key_press(self, symbol: int, modifiers: int):
        if not self.GAME_PAUSE:
            if not self.leftkey:
                if symbol == arcade.key.LEFT:
                    self.db_left.change()
            else:
                if symbol == self.leftkey:
                    self.db_left.change()
            if not self.rightkey:
                if symbol == arcade.key.RIGHT:
                    self.db_right.change()
            else:
                if symbol == self.rightkey:
                    self.db_right.change()

    def on_key_release(self, symbol: int, modifiers: int):
        if not self.GAME_PAUSE:
            if not self.leftkey:
                if symbol == arcade.key.LEFT:
                    self.db_left.change()
            else:
                if symbol == self.leftkey:
                    self.db_left.change()
            if not self.rightkey:
                if symbol == arcade.key.RIGHT:
                    self.db_right.change()
            else:
                if symbol == self.rightkey:
                    self.db_right.change()

    def go(self):

        arcade.run()
