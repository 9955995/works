import pygame
from pygame.sprite import Sprite

class Peashooter(Sprite):
    def __init__(self,ai_setting,screen):
        """初始化豌豆射手并设置其初始化位置"""
        super().__init__();
        self.screen=screen;
        self.ai_setting=ai_setting;
        
        #加载射手图像并获取其外接矩形
        self.image=pygame.image.load('images/peashooter.bmp');
        self.rect=self.image.get_rect();
        self.screen_rect=screen.get_rect();
        
        #将每个新射手放在屏幕左边中央
        self.rect.centery=self.screen_rect.centery;
        self.rect.left=self.screen_rect.left;
        
        #在射手的属性center中存储小数值
        self.center=float(self.rect.centery);
        
        #移动标志
        self.moving_up=False;
        self.moving_down=False;
        
    def update(self):
        """根据移动标志调整位置"""
        #更新射手的center值，而不是rect
        if self.moving_down and self.rect.bottom<self.screen_rect.bottom:
            self.center+=self.ai_setting.peashooter_speed_factor;
        if self.moving_up and self.rect.top>0:
            self.center-=self.ai_setting.peashooter_speed_factor;
        
        #根据self.center更新rect对象
        self.rect.centery=self.center;
        
    def blitme(self):
        """在指定位置绘制射手"""
        self.screen.blit(self.image,self.rect);
        
        
