import pygame as pg
import os
from .. import tool
from .. import constants as c

class Menu(tool.State):
    
    def __init__(self):
        tool.State.__init__(self)
    
    def startup(self, current_time, persist):
        self.next = c.LEVEL
        self.persist = persist
        self.game_info = persist
        self.setupBackground()
        self.setupOptions()
        self.setupOptionMenu()
        pg.mixer.music.stop()
        pg.mixer.music.load(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))) ,"resources", "music", "intro.opus"))
        pg.mixer.music.play(-1, 0)
        pg.display.set_caption(c.ORIGINAL_CAPTION)

    def setupBackground(self):
        frame_rect = (80, 0, 800, 600)
        # 1、形参中加单星号，即f(*x)则表示x为元组，所有对x的操作都应将x视为元组类型进行。
        # 2、双星号同上，区别是x视为字典。
        # 3、在变量前加单星号表示将元组（列表、集合）拆分为单个元素。
        # 4、双星号同上，区别是目标为字典，字典前加单星号的话可以得到“键”。
        self.bg_image = tool.get_image(tool.GFX[c.MAIN_MENU_IMAGE], *frame_rect)
        self.bg_rect = self.bg_image.get_rect()
        self.bg_rect.x = 0
        self.bg_rect.y = 0
        
    def setupOptions(self):
        # 冒险模式
        self.adventure_frames = []
        frame_names = (f'{c.OPTION_ADVENTURE}_0', f'{c.OPTION_ADVENTURE}_1')
        frame_rect = (0, 0, 330, 144)
        
        for name in frame_names:
            self.adventure_frames.append(tool.get_image_menu(tool.GFX[name], *frame_rect, c.BLACK, 1))
        self.adventure_frame_index = 0
        self.adventure_image = self.adventure_frames[self.adventure_frame_index]
        self.adventure_rect = self.adventure_image.get_rect()
        self.adventure_rect.x = 400
        self.adventure_rect.y = 60
        self.adventure_highlight_time = 0
        
        # 退出按钮
        self.exit_frames = []
        exit_frame_names = (f'{c.EXIT}_0', f'{c.EXIT}_1')
        exit_frame_rect = (0, 0, 47, 27)
        for name in exit_frame_names:
            self.exit_frames.append(tool.get_image_menu(tool.GFX[name], *exit_frame_rect, c.BLACK, 1.1))
        self.exit_frame_index = 0
        self.exit_image = self.exit_frames[self.exit_frame_index]
        self.exit_rect = self.exit_image.get_rect()
        self.exit_rect.x = 730
        self.exit_rect.y = 507
        self.exit_highlight_time = 0

        # 选项按钮
        self.option_button_frames = []
        option_button_frame_names = (f'{c.OPTION_BUTTON}_0', f'{c.OPTION_BUTTON}_1')
        option_button_frame_rect = (0, 0, 81, 31)
        for name in option_button_frame_names:
            self.option_button_frames.append(tool.get_image_menu(tool.GFX[name], *option_button_frame_rect, c.BLACK))
        self.option_button_frame_index = 0
        self.option_button_image = self.option_button_frames[self.option_button_frame_index]
        self.option_button_rect = self.option_button_image.get_rect()
        self.option_button_rect.x = 560
        self.option_button_rect.y = 490
        self.option_button_hightlight_time = 0

        # 小游戏
        self.littleGame_frames = []
        littleGame_frame_names = (c.LITTLEGAME_BUTTON + '_0', c.LITTLEGAME_BUTTON + '_1')
        littleGame_frame_rect = (0, 7, 317, 135)
        for name in littleGame_frame_names:
            self.littleGame_frames.append(tool.get_image_menu(tool.GFX[name], *littleGame_frame_rect, c.BLACK, 1))
        self.littleGame_frame_index = 0
        self.littleGame_image = self.littleGame_frames[self.littleGame_frame_index]
        self.littleGame_rect = self.littleGame_image.get_rect()
        self.littleGame_rect.x = 397
        self.littleGame_rect.y = 175
        self.littleGame_highlight_time = 0

        self.adventure_start = 0
        self.adventure_timer = 0
        self.adventure_clicked = False
        self.option_button_clicked = False

    def inAreaAdventure(self, x, y):
        if (x >= self.adventure_rect.x and x <= self.adventure_rect.right and
            y >= self.adventure_rect.y and y <= self.adventure_rect.bottom):
            return True
        else:
            return False
    
    def inAreaExit(self, x, y):
        if (x >= self.exit_rect.x and x <= self.exit_rect.right and
            y >= self.exit_rect.y and y <= self.exit_rect.bottom):
            return True
        else:
            return False
    
    def inAreaOptionButton(self, x, y):
        if (x >= self.option_button_rect.x and x <= self.option_button_rect.right and
            y >= self.option_button_rect.y and y <= self.option_button_rect.bottom):
            return True
        else:
            return False
    
    def inAreaLittleGame(self, x, y):
        if (x >= self.littleGame_rect.x and x <= self.littleGame_rect.right and
            y >= self.littleGame_rect.y and y <= self.littleGame_rect.bottom):
            return True
        else:
            return False

    def checkHilight(self, x, y):
        # 高亮冒险模式按钮
        if self.inAreaAdventure(x, y):
            self.adventure_highlight_time = self.current_time
        # 高亮退出按钮
        elif self.inAreaExit(x, y):
            self.exit_highlight_time = self.current_time
        # 高亮选项按钮
        elif self.inAreaOptionButton(x, y):
            self.option_button_hightlight_time = self.current_time
        # 高亮小游戏按钮
        elif self.inAreaLittleGame(x, y):
            self.littleGame_highlight_time = self.current_time

        # 检查是否应当高亮并应用结果
        if (self.current_time - self.adventure_highlight_time) < 80:
            self.adventure_frame_index = 1
        else:
            self.adventure_frame_index = 0
        self.adventure_image = self.adventure_frames[self.adventure_frame_index]
        if (self.current_time - self.exit_highlight_time) < 80:
            self.exit_frame_index = 1
        else:
            self.exit_frame_index = 0
        self.exit_image = self.exit_frames[self.exit_frame_index]
        if (self.current_time - self.option_button_hightlight_time) < 80:
            self.option_button_frame_index = 1
        else:
            self.option_button_frame_index = 0
        self.option_button_image = self.option_button_frames[self.option_button_frame_index]
        if (self.current_time - self.littleGame_highlight_time) < 80:
            self.littleGame_frame_index= 1
        else:
            self.littleGame_frame_index = 0
        self.littleGame_image = self.littleGame_frames[self.littleGame_frame_index]

    def checkAdventureClick(self, mouse_pos):
        x, y = mouse_pos
        if self.inAreaAdventure(x, y):
            self.adventure_clicked = True
            self.adventure_timer = self.adventure_start = self.current_time
            self.persist[c.GAME_MODE] = c.MODE_ADVENTURE
            # 播放进入音效
            pg.mixer.Sound(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))) ,"resources", "sound", "evillaugh.ogg")).play()
            pg.mixer.Sound(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))) ,"resources", "sound", "lose.ogg")).play()
    
    # 点击到按钮，修改转态的done属性
    def checkExitClick(self, mouse_pos):
        x, y = mouse_pos
        if self.inAreaExit(x, y):
            self.done = True
            self.next = c.EXIT

    # 检查有没有按到小游戏
    def checkLittleGameClick(self, mouse_pos):
        x, y = mouse_pos
        if self.inAreaLittleGame(x, y):
            self.done = True
            self.persist[c.GAME_MODE] = c.MODE_LITTLEGAME
            # 播放点击音效
            pg.mixer.Sound(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))) ,"resources", "sound", "buttonclick.ogg")).play()

    def setupOptionMenu(self):
        # 选项菜单框
        frame_rect = (0, 0, 500, 500)
        self.big_menu = tool.get_image_menu(tool.GFX[c.BIG_MENU], *frame_rect, c.BLACK, 1.1)
        self.big_menu_rect = self.big_menu.get_rect()
        self.big_menu_rect.x = 150
        self.big_menu_rect.y = 0

        # 返回按钮
        frame_rect = (0, 0, 342, 87)
        self.return_button = tool.get_image_menu(tool.GFX[c.RETURN_BUTTON], *frame_rect, c.BLACK, 1.1)
        self.return_button_rect = self.return_button.get_rect()
        self.return_button_rect.x = 220
        self.return_button_rect.y = 440

        # 音量+、音量-
    
    def checkOptionButtonClick(self, mouse_pos):
        x, y = mouse_pos
        if self.inAreaOptionButton(x, y):
            self.option_button_clicked = True
            # 播放点击音效
            pg.mixer.Sound(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))) ,"resources", "sound", "buttonclick.ogg")).play()

    # 在选项菜单打开时，检测是否点击到返回
    def checkReturnClick(self, mouse_pos):
        x, y = mouse_pos
        if (x >= self.return_button_rect.x and x <= self.return_button_rect.right and
            y >= self.return_button_rect.y and y <= self.return_button_rect.bottom):
            return True
        return False

    def update(self, surface, current_time, mouse_pos, mouse_click):
        self.current_time = self.game_info[c.CURRENT_TIME] = current_time
        
        surface.blit(self.bg_image, self.bg_rect)
        surface.blit(self.adventure_image, self.adventure_rect)
        surface.blit(self.exit_image, self.exit_rect)
        surface.blit(self.option_button_image, self.option_button_rect)
        surface.blit(self.littleGame_image, self.littleGame_rect)

        # 没有选到选项时，检查有没有点到选项
        if self.adventure_clicked:
            # 点到后播放动画
            if (self.current_time - self.adventure_timer) > 150:
                self.adventure_frame_index += 1
                if self.adventure_frame_index >= 2:
                    self.adventure_frame_index = 0
                self.adventure_timer = self.current_time
                self.adventure_image = self.adventure_frames[self.adventure_frame_index]
            if (self.current_time - self.adventure_start) > 3200:
                self.done = True
        elif self.option_button_clicked:
            surface.blit(self.big_menu, self.big_menu_rect)
            surface.blit(self.return_button, self.return_button_rect)
            if (mouse_pos and self.checkReturnClick(mouse_pos)):
                self.option_button_clicked = False
                pg.mixer.Sound(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))) ,"resources", "sound", "buttonclick.ogg")).play()
        else:
            # 先检查选项高亮预览
            self.checkHilight(*pg.mouse.get_pos())
            if mouse_pos:
                self.checkExitClick(mouse_pos)
                self.checkOptionButtonClick(mouse_pos)
                self.checkLittleGameClick(mouse_pos)
                self.checkAdventureClick(mouse_pos)
