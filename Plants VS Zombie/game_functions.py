import sys
import pygame
from pea import Pea
from zombie import Zombie
from boss import Boss
from time import sleep
import json
from random import randint
import pygame.mixer
import time

def check_keydown_events(event,ai_setting,screen,status,peashooter,peas):
    """响应按键"""
    if event.key==pygame.K_UP:
        peashooter.moving_up=True;
    elif event.key==pygame.K_DOWN:
        peashooter.moving_down=True;
    elif event.key==pygame.K_SPACE:
        throw_peas(ai_setting,screen,peashooter,peas);
    elif event.key==pygame.K_q:
        with open(ai_setting.filename,'w') as file_object:
            json.dump(status.high_score,file_object);
        with open(ai_setting.player_filename,'a') as player_file_object:
            localtime = time.asctime(time.localtime(time.time()));
            data=localtime+'-----Score: '+str(status.score);
            json.dump(data,player_file_object);
        sys.exit();
        
        
def check_keyup_events(event,peashooter):
    """响应松开"""
    if event.key==pygame.K_UP:
        peashooter.moving_up=False;
    elif event.key==pygame.K_DOWN:
        peashooter.moving_down=False;


def check_events(ai_setting,screen,status,scoreboard,play_button,exit_button,peashooter,zombies,peas):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            with open(ai_setting.filename,'w') as file_object:
                json.dump(status.high_score,file_object);
            with open(ai_setting.player_filename,'a') as player_file_object:
                localtime = time.asctime(time.localtime(time.time()));
                data=localtime+'-----Score: '+str(status.score);
                json.dump(data,player_file_object);
            sys.exit();
            
        elif event.type==pygame.KEYDOWN:
            check_keydown_events(event,ai_setting,screen,status,peashooter,peas);
                
        elif event.type==pygame.KEYUP:
            check_keyup_events(event,peashooter)

        elif event.type==pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y=pygame.mouse.get_pos();
            check_play_button(ai_setting,screen,status,scoreboard,play_button,peashooter,zombies,peas,mouse_x,mouse_y);
            check_exit_button(ai_setting,status,exit_button,mouse_x,mouse_y);


def check_play_button(ai_setting,screen,status,scoreboard,play_button,peashooter,zombies,peas,mouse_x,mouse_y):
    """在玩家单击Play按钮时开始新游戏"""
    button_clicked=play_button.rect.collidepoint(mouse_x,mouse_y);
    if button_clicked and not status.game_active:
        start_game(ai_setting,screen,status,scoreboard,peashooter,zombies,peas);
 
   
def check_exit_button(ai_setting,status,exit_button,mouse_x,mouse_y):
    """在玩家单击Exit按钮时退出游戏"""
    button_clicked=exit_button.rect.collidepoint(mouse_x,mouse_y);
    if button_clicked:
        with open(ai_setting.filename,'w') as file_object:
            json.dump(status.high_score,file_object);
        with open(ai_setting.player_filename,'a') as player_file_object:
            localtime = time.asctime(time.localtime(time.time()));
            data=localtime+'-----Score: '+str(status.score);
            json.dump(data,player_file_object);
        sys.exit();


def start_game(ai_setting,screen,status,scoreboard,peashooter,zombies,peas):
    """操纵新游戏的开始"""
    #重置游戏设置
    ai_setting.initialize_dynamic_setting();
    #隐藏光标
    pygame.mouse.set_visible(False);
    #重置游戏统计信息
    status.reset_status();
    status.game_active=True;    
    #重置记分牌图像
    scoreboard.prep_images();    
    #清空僵尸列表和豌豆列表
    zombies.empty();
    peas.empty();
    #让射手居中
    peashooter.center=screen.get_rect().centery;    
    #改变背景音乐
    pygame.mixer.music.load("coming.wav")
    pygame.mixer.music.play();
    #切换背景图像
    change_background(ai_setting,screen,status)
   
   
def change_background(ai_setting,screen,status):
    """根据不同的情景切换背景图像"""
    if status.game_active:
        ai_setting.background = pygame.image.load('images/bg'+str(status.level)+'.bmp').convert()
    else:
        ai_setting.background = pygame.image.load('images/fail.bmp').convert()
    
        
def update_screen(ai_setting,screen,status,scoreboard,peashooter,zombies,bossGroup,peas,play_button,exit_button):
    """更新屏幕上的图像，并初始化带新屏幕"""
    screen.blit(ai_setting.background,(0,0))
    
    if status.game_active and status.level<7:
        #在射手和僵尸后面绘制所有豌豆
        for pea in peas.sprites():
            pea.blit_pea();
        peashooter.blitme();
        zombies.draw(screen);
        bossGroup.draw(screen);
        #显示得分
        scoreboard.show_score();
        
    if status.game_active and status.level==7:
        scoreboard.score_rect.x=350;
        scoreboard.score_rect.top=250;
        scoreboard.high_score_rect.x=350;
        scoreboard.high_score_rect.top=350;
        #显示部分信息
        scoreboard.show_final();
    
    #如果游戏处于非活动状态，就绘制Play按钮
    if not status.game_active:
        pygame.mouse.set_visible(True);
        play_button.draw_button();
        exit_button.draw_button();
                
    #让最近绘制的屏幕可见
    pygame.display.flip();
    
    if not pygame.mixer.music.get_busy() and status.level<7: 
        pygame.mixer.music.load("bg.wav")
        pygame.mixer.music.play(-1);


def update_peas(ai_setting,screen,status,scoreboard,soundwav,peashooter,zombies,bossGroup,peas):
    """更新豌豆的位置，并删除已经消失的豌豆"""
    #更新豌豆 的位置
    peas.update();
    
    #删除消失的豌豆
    for pea in peas.copy():
        if pea.rect.left>=screen.get_rect().right:
            peas.remove(pea);
    check_peas_zombies_collisions(ai_setting,screen,status,scoreboard,soundwav,peashooter,zombies,bossGroup,peas);
    check_peas_boss_collisions(ai_setting,screen,status,scoreboard,soundwav,peashooter,zombies,bossGroup,peas);
    

def check_peas_zombies_collisions(ai_setting,screen,status,scoreboard,soundwav,peashooter,zombies,bossGroup,peas):    
    """响应豌豆和僵尸的碰撞"""
    #删除发生碰撞的豌豆和僵尸
    collisions=pygame.sprite.groupcollide(peas,zombies,True,True);
    
    if collisions:
        for zombies in collisions.values():
            status.score+=ai_setting.zombie_point*len(zombies);
            scoreboard.prep_score();
            soundwav.play();
        check_high_score(status,scoreboard);

    if ai_setting.zombie_number==0 and len(zombies)==0:
        start_new_level(ai_setting,screen,status,scoreboard,peashooter,zombies,bossGroup,peas);
    
def check_peas_boss_collisions(ai_setting,screen,status,scoreboard,soundwav,peashooter,zombies,bossGroup,peas):    
    """响应豌豆和僵尸boss的碰撞"""
    #删除发生碰撞的豌豆和僵尸boss
    collisions=pygame.sprite.groupcollide(peas,bossGroup,True,True);
    
    if collisions:
        for bossGroup in collisions.values():
            status.score+=ai_setting.boss_point*len(bossGroup);
            scoreboard.prep_score();
            soundwav.play();
        check_high_score(status,scoreboard);
    
    if ai_setting.boss_time==0 and len(bossGroup)==0 and status.level<7:
        start_new_level(ai_setting,screen,status,scoreboard,peashooter,zombies,bossGroup,peas);
        
      
def start_new_level(ai_setting,screen,status,scoreboard,peashooter,zombies,bossGroup,peas):
    """开始新的等级游戏"""
    #删除现有的豌豆,并提高一个等级
    peas.empty();
    #加快游戏节奏
    ai_setting.increase_speed();
    
    #提高等级
    status.level+=1;
    scoreboard.prep_level();
    
    #切换背景图像
    change_background(ai_setting,screen,status);
    
    if status.level==6:
        #改变背景音乐
        pygame.mixer.music.load("coming.wav")
        pygame.mixer.music.play();
 
    
def throw_peas(ai_setting,screen,peashooter,peas):
    """创建一个拳头，并将其加入到编组peas中"""
    if len(peas)<ai_setting.peas_allowed:
        new_pea=Pea(ai_setting,screen,peashooter);
        peas.add(new_pea);


def create_zombie(ai_setting,screen,zombies):
    """创建一个僵尸"""
    zombie=Zombie(ai_setting,screen);
    zombie.rect.y=randint(zombie.rect.height,600-zombie.rect.height);
    zombies.add(zombie);
    ai_setting.zombie_number-=1;


def create_zombies(ai_setting,screen,status,zombies):
    """创建一群僵尸"""
    if ai_setting.zombie_number>0:
        if len(zombies)==0:
            create_zombie(ai_setting,screen,zombies);
        for zombie in zombies.sprites():
            if zombie.rect.x<250*ai_setting.zombie_number:
                zombie.rect.y+=randint(-100,100);
                create_zombie(ai_setting,screen,zombies);
                break;

def update_zombies(ai_setting,status,screen,scoreboard,peashooter,zombies,bossGroup,peas):
    """更新所有僵尸的位置"""
    if status.level<6:
        zombies.update();
        create_zombies(ai_setting,screen,status,zombies);
        
        #检测射手和僵尸的碰撞
        if pygame.sprite.spritecollideany(peashooter,zombies):
            peashooter_hit(ai_setting,status,screen,scoreboard,peashooter,zombies,bossGroup,peas);
        
        #检查是否有僵尸到达屏幕左端
        check_zombies_left(ai_setting,status,screen,scoreboard,peashooter,zombies,bossGroup,peas);


def create_boss_group(ai_setting,screen,bossGroup):
    """创建一群僵尸boss"""
    if ai_setting.boss_time>0:
        boss=Boss(ai_setting,screen);
        y_number=int((600-boss.rect.height)/boss.rect.height);
        
        if len(bossGroup)==0:
            boss=Boss(ai_setting,screen);
            bossGroup.add(boss);
        else:
            for m in range(2):
                for n in range(y_number):
                    boss=Boss(ai_setting,screen);
                    boss.x=1000+(100*m);
                    boss.rect.y=(n+1)*boss.rect.height;
                    bossGroup.add(boss);
                    ai_setting.boss_time=0;


def update_bossGroup(ai_setting,status,screen,scoreboard,peashooter,zombies,bossGroup,peas):
    """更新boss的位置"""
    if status.level==6:
        bossGroup.update();
        create_boss_group(ai_setting,screen,bossGroup);
        
        #检测射手和僵尸boss的碰撞
        if pygame.sprite.spritecollideany(peashooter,bossGroup):
            peashooter_hit_boss(ai_setting,status,screen,scoreboard,peashooter,zombies,bossGroup,peas);
        
        #检查是否有僵尸boss到达屏幕左端
        check_boss_left(ai_setting,status,screen,scoreboard,peashooter,zombies,bossGroup,peas);
    
 
def peashooter_hit(ai_setting,status,screen,scoreboard,peashooter,zombies,bossGroup,peas):
    """响应被僵尸撞到的射手"""
    if status.peashooter_left>0:
        status.peashooter_left-=1;
        #更新记分牌
        status.level=1;
        scoreboard.prep_level();
        scoreboard.prep_bloods();
        #清空僵尸列表和豌豆列表
        zombies.empty();
        bossGroup.empty();
        peas.empty();
        #重置游戏设置
        ai_setting.initialize_dynamic_setting();        
        #将射手放到屏幕左边中央
        peashooter.center=screen.get_rect().centery;
        #切换背景图像
        change_background(ai_setting,screen,status)
        #暂停
        sleep(0.5);
    else:
        status.game_active=False;
        #显示隐藏的光标
        pygame.mouse.set_visible(True);
        #切换背景图像
        change_background(ai_setting,screen,status)

def check_zombies_left(ai_setting,status,screen,scoreboard,peashooter,zombies,bossGroup,peas):
    """检查是否有僵尸到达了屏幕左端"""
    for zombie in zombies.sprites():
        if zombie.rect.right<=screen.get_rect().left:
             peashooter_hit(ai_setting,status,screen,scoreboard,peashooter,zombies,bossGroup,peas);
             break;
             
             
def peashooter_hit_boss(ai_setting,status,screen,scoreboard,peashooter,zombies,bossGroup,peas):
    """响应被僵尸boss撞到的射手"""
    peashooter_hit(ai_setting,status,screen,scoreboard,peashooter,zombies,bossGroup,peas);


def check_boss_left(ai_setting,status,screen,scoreboard,peashooter,zombies,bossGroup,peas):
    """检查是否有僵尸boss到达了屏幕左端"""
    for boss in bossGroup.sprites():
        if boss.rect.right<=screen.get_rect().left:
            peashooter_hit_boss(ai_setting,status,screen,scoreboard,peashooter,zombies,bossGroup,peas);
            break;
             
def check_high_score(status,scoreboard):
    """检查是否诞生了新的最高得分"""
    if status.score>status.high_score:
        status.high_score=status.score;
        scoreboard.prep_high_score();

        
