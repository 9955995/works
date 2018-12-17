import pygame
from settings import Setting
from peashooter import Peashooter
import game_functions as gf
from pygame.sprite import Group
from game_status import GameStatus
from button import Button
from scoreboard import Scoreboard
import pygame.mixer
from prompt import Prompt

def run_game():
    #初始化游戏并创建一个屏幕对象
    pygame.init();
    pygame.mixer.init();
    screen=pygame.display.set_mode((1000,600));
    pygame.display.set_caption("Plants VS Zombie");
    ai_setting=Setting();
    
    #声音的设置
    soundwav=pygame.mixer.Sound("boom.wav")
    pygame.mixer.music.load("first.wav")
    pygame.mixer.music.play(-1);
    
    #创建play按钮
    play_button=Button(ai_setting,screen,"Play",400);
    exit_button=Button(ai_setting,screen,"Exit",500);
    
    #创建一个射手,一个豌豆编组，一个僵尸编组和一个僵尸Boss编组
    peashooter=Peashooter(ai_setting,screen);
    peas=Group();
    zombies=Group();
    bossGroup=Group();
    
    #创建一个用于存储游戏统计信息的实例，并创建记分牌
    status=GameStatus(ai_setting);
    scoreboard=Scoreboard(ai_setting,screen,status);
    
    #开始游戏的主循环
    while True:
        
        gf.check_events(ai_setting,screen,status,scoreboard,play_button,exit_button,peashooter,zombies,peas);
        
        if status.game_active:
            peashooter.update();
            gf.update_peas(ai_setting,screen,status,scoreboard,soundwav,peashooter,zombies,bossGroup,peas);
            gf.update_zombies(ai_setting,status,screen,scoreboard,peashooter,zombies,bossGroup,peas);
            gf.update_bossGroup(ai_setting,status,screen,scoreboard,peashooter,zombies,bossGroup,peas);
        
        gf.update_screen(ai_setting,screen,status,scoreboard,peashooter,zombies,bossGroup,peas,play_button,exit_button);

run_game();
