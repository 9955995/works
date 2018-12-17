import pygame
from pygame.sprite import Sprite

class Zombie(Sprite):
    """表示单个僵尸的类"""
    
    def __init__(self,ai_setting,screen):
        """初始化僵尸并设置其起始位置"""
        super().__init__();
        self.screen=screen;
        self.ai_setting=ai_setting;
        
        #加载僵尸图像
        self.image=pygame.image.load('images/zombie.bmp');
        self.rect=self.image.get_rect();
          
        #每个僵尸最初都在屏幕右上角
        self.rect.x=self.ai_setting.screen_width;
        self.rect.y=0;
        
        #存储僵尸的准确位置
        self.x=float(self.rect.x);
        
    def blitme(self):
        """在指定位置绘制僵尸"""
        self.screen.blit(self.image,self.rect);
        
    def update(self):
        """移动僵尸"""
        self.x-=self.ai_setting.zombie_speed_factor;
        self.rect.x=self.x;
        
