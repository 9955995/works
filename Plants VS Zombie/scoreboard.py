import pygame.font
from pygame.sprite import Group
from blood import Blood

class Scoreboard():
    """显示得分信息的类"""
    def __init__(self,ai_setting,screen,status):
        """初始化显示得分涉及的属性"""
        self.screen=screen;
        self.screen_rect=screen.get_rect();
        self.ai_setting=ai_setting;
        self.status=status;
        
        #显示得分信息时使用的字体设置
        self.text_color=(255,255,0);
        self.bg_color=(0,250,0);
        self.font=pygame.font.SysFont("arial",30);
        
        #准备初始得分图像
        self.prep_images();
        
    def prep_images(self):
        self.prep_score();
        self.prep_high_score();
        self.prep_level();
        self.prep_bloods();
        
    def prep_score(self):
        """将得分转换为一幅渲染的图像"""
        #字符串格式设置指令
        score_str="Score: "+"{:,}".format(self.status.score);
        self.score_image=self.font.render(score_str,True,self.text_color);
        
        #将得分放在屏幕顶部
        self.score_rect=self.score_image.get_rect();
        self.score_rect.x=400;
        self.score_rect.top=15;
    
    def prep_high_score(self):
        """将最高得分转换为一幅渲染的图像"""
        high_score_str="High Score: "+"{:,}".format(self.status.high_score);
        self.high_score_image=self.font.render(high_score_str,True,self.text_color);
        
        #将最高得分放在屏幕顶部
        self.high_score_rect=self.high_score_image.get_rect();
        self.high_score_rect.x=135;
        self.high_score_rect.top=15;
        
    def prep_level(self):
       """将等级装换为渲染的图像"""
       self.level_str="Level: "+str(self.status.level);
       self.level_image=self.font.render(self.level_str,True,self.text_color);
       
       #将等级放在得分右边
       self.level_rect=self.level_image.get_rect();
       self.level_rect.left=600;
       self.level_rect.top=self.score_rect.top;
    
    def prep_bloods(self):
        """显示还剩多少血"""
        self.bloods=Group();
        for number in range(self.status.peashooter_left):
            blood=Blood(self.ai_setting,self.screen);
            blood.rect.right=self.screen.get_rect().right-number*blood.rect.width;
            blood.rect.top=self.screen.get_rect().top;
            self.bloods.add(blood);
    
    def show_score(self):
        """在屏幕上显示得分"""
        self.screen.blit(self.score_image,self.score_rect);
        self.screen.blit(self.high_score_image,self.high_score_rect);
        self.screen.blit(self.level_image,self.level_rect);
        self.bloods.draw(self.screen);
        
    def show_final(self):
        """游戏成功显示的信息"""
        self.screen.blit(self.score_image,self.score_rect);
        self.screen.blit(self.high_score_image,self.high_score_rect);
