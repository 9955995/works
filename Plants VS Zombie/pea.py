import pygame
from pygame.sprite import Sprite

class Pea(Sprite):
    """一个对僵尸的射击进行管理的类"""
    def __init__(self,ai_setting,screen,hero):
        """在射手处的位置创建一个豌豆对象"""
        super().__init__();
        self.screen=screen;
        self.ai_setting=ai_setting;
        
        #创建一个表示豌豆的矩形，再设置正确的位置
        self.image=pygame.image.load('images/pea.bmp');
        self.rect=self.image.get_rect();
        self.rect.centery=hero.rect.centery;
        self.rect.left=hero.rect.right;
        
        #存储用小数表示的豌豆位置
        self.x=float(self.rect.x);

    
    def update(self):
        """向右移动豌豆"""
        #更新表示拳头位置的小数值
        self.x+=self.ai_setting.pea_speed_factor;
        #更新表示豌豆的rect的位置
        self.rect.x=self.x;
    
    def blit_pea(self):
        """在屏幕上绘制豌豆"""
        self.screen.blit(self.image,self.rect);
