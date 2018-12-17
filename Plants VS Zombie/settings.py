import pygame

class Setting():
    """存储所有设置的类"""
    
    def __init__(self):
        """初始化游戏的静态设置"""
        #屏幕设置
        self.screen_width=1000;
        self.screen_height=600;
        self.bg_color=(230,230,230);
        self.background = pygame.image.load('images/bg.bmp').convert()
        
        #豌豆射手的设置
        self.peashooter_limit=2;
        
        #豌豆设置
        self.peas_allowed=5;
        
        #以怎样的速度加快游戏节奏
        self.speedup_scale=1.5;

        #僵尸点数的提高
        self.score_scale=2;
        
        #存储数据的文件
        self.filename='high_score.json'
        self.player_filename='history.json'
        
        self.initialize_dynamic_setting();
        
    def initialize_dynamic_setting(self):
        """初始化随游戏进行而变化的设置"""
        self.peashooter_speed_factor=0.3;
        self.pea_speed_factor=2;
        self.zombie_speed_factor=0.1;
        self.zombie_number=3;
        #记分
        self.zombie_point=10;
        
        #boss的设置
        self.boss_speed_factor=0.2;
        self.boss_time=1;
        self.boss_point=100;
        
    def increase_speed(self):
        """提高速度设置和僵尸点数"""
        self.peashooter_speed_factor*=self.speedup_scale;
        self.pea_speed_factor*=self.speedup_scale;
        self.zombie_speed_factor*=self.speedup_scale;
        self.zombie_point*=self.score_scale;
        self.zombie_number=2;
