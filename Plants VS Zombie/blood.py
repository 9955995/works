import pygame
from pygame.sprite import Sprite

class Blood(Sprite):
    def __init__(self,ai_setting,screen):
        """初始化并设置其初始化位置"""
        super().__init__();
        self.screen=screen;
        self.ai_setting=ai_setting;
        
        #加载图像并获取其外接矩形
        self.image=pygame.image.load('images/flower.bmp');
        self.rect=self.image.get_rect();
        self.screen_rect=screen.get_rect();
        
        #初始化将其放在屏幕底中央
        self.rect.centerx=self.screen_rect.centerx;
        self.rect.bottom=self.screen_rect.bottom;
        
        #属性center中存储小数值
        self.center=float(self.rect.centerx);
        
    def blitme(self):
        """在指定位置绘制"""
        self.screen.blit(self.image,self.rect);
        
        

