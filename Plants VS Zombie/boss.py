import pygame
from pygame.sprite import Sprite

class Boss(Sprite):
    """表示僵尸Boss的类"""
    
    def __init__(self,ai_setting,screen):
        """初始化僵尸Boss并设置其起始位置"""
        super().__init__();
        self.screen=screen;
        self.ai_setting=ai_setting;
        
        #加载僵尸Boss图像
        self.image=pygame.image.load('images/boss.bmp');
        self.rect=self.image.get_rect();
          
        #每个僵尸最初都在屏幕右上角
        self.rect.x=900;
        self.rect.y=250;
        
        #存储僵尸的准确位置
        self.x=float(self.rect.x);
        
    def blitme(self):
        """在指定位置绘制僵尸boss"""
        self.screen.blit(self.image,self.rect);
        
    def update(self):
        """移动僵尸boss"""
        self.x-=self.ai_setting.boss_speed_factor;
        self.rect.x=self.x;
        

