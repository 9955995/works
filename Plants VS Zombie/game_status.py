import json

class GameStatus():
    """跟踪游戏的统计信息"""
    def __init__(self,ai_setting):
        self.ai_setting=ai_setting;
        self.reset_status();
        
        #让游戏开始处于非活动状态
        self.game_active=False;
        
        #在任何情况都不应重置最高得分
        #self.high_score=0;
        with open(ai_setting.filename) as file_object:
            self.high_score=json.load(file_object);
        
    
    def reset_status(self):
        """初始化在游戏运行期间可能变化的统计信息"""
        self.peashooter_left=self.ai_setting.peashooter_limit;
        self.score=0;
        self.level=1;
