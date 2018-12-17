import pygame.font

class Prompt():
    
    def __init__(self,ai_setting,screen,msg):
        """初始化按钮的属性"""
        self.screen=screen;
        self.screen_rect=screen.get_rect();
        
        #设置提示的尺寸和其他属性
        self.width,self.height=500,200;
        self.text_color=(255,255,255);
        self.font=pygame.font.SysFont("arial",150);#默认为None
        
        #创建提示的rect对象，并使其居中
        self.rect=pygame.Rect(0,0,self.width,self.height);
        self.rect.centerx=self.screen_rect.centerx;
        self.rect.y=100;
        
        #提示的标签只需创建一次
        self.prep_msg(msg);
        
        #设置标志
        self.flag=False;


    def prep_msg(self,msg):
        """将msg渲染为图像，并将其在提示上居中"""
        self.msg_image=self.font.render(msg,True,self.text_color);
        self.msg_image_rect=self.msg_image.get_rect();
        self.msg_image_rect.centerx=self.rect.centerx;
        self.msg_image_rect.y=self.rect.y;


    def draw_prompt(self):
        """绘制一个用颜色填充的提示，再绘制文本"""
        self.screen.blit(self.msg_image,self.msg_image_rect);

