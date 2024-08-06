import random
import json
import time 
import numpy as np
import torch 

class Filed():
    def __init__(self):
        # 現在のプレイヤー
        self.now_player:int = 0 # 1 or 2をとる

        # 手持ちのカード
        self.hand = {1:[], 2:[]}
        # フィールドに出されているカード
        self.field_card:list[tuple[int,int]] = []
        # フィールドにストックしてあるカード
        self.field_stock:list[tuple[int,int]] = []
        # すでにとったカード
        self.pile:dict[int,list[tuple[int,int]]] = {1:[], 2:[]}
        # 役がそろったときに扱う
        self.yaku : dict[int,list[int]] = {1:[],2:[]}
        # round を数える
        self.round : int = 0
        # koikoi_num
        self.koikoi = {1:[0,0,0,0,0,0,0,0], 2:[0,0,0,0,0,0,0,0]}
        # 前回ゲームの勝者を保持する
        self.winner = None
        # logを表示する Ture->ログの非表示 False->ログの表示
        self.silence = False
        
        # 卓が行うこと
        self.state = 'init'
        self.__deal_card()
        
    
    def turn_player(self):
        # action最初のプレイヤーを決める
        if self.winner == None:
            self.now_player = random.randint(1,2)
        else:
            self.now_player = self.winner
        return 
                   
    def __deal_card(self):
        # action
        # 4枚のスーツが全て同じ場所に来ないように配りなおす
        while True:
            card: list[tuple[int, int]] = [(ii+1,jj+1) for ii in range(12) for jj in range (4)]
            random.shuffle(card)
            self.hand[1] = sorted(card[0:8])
            self.hand[2] = sorted(card[8:16])
            self.field_slot = sorted(card[16:24])
            self.stock = card[24:]
            # check hand-4 and board-4          
            flag = True
            for suit in range(1,13):
                if 4 in [[card[0] for card in self.hand[1]].count(suit),
                         [card[0] for card in self.hand[2]].count(suit),
                         [card[0] for card in self.field_card].count(suit)]:
                    flag = False        
            if flag:
                break
            
            
        # next state
        self.__write_log()   
        self.state = 'discard'
        
        return
    
    @property
    def pairing_card(self):
        """
        @propery
        場で見せたカードとペアにできるカードのリストを返すプロパティ
        """
        return [card for card in self.field_card if card[0] == self.show[0][0]]
        
    def discard(self, card:tuple=(0,0)):  
        """"
        stateがdiscardの時だけ呼び出しが可能
        次のstateはdiscard-pickに移行する
        
        """      
        assert self.state == 'discard'
        assert card in self.hand[self.now_player]
        # action
        self.turn_point = self.yaku_point(self.turn_player)
        ind = self.hand[self.turn_player].index(card)
        self.show = [self.hand[self.turn_player].pop(ind)]
        # next state
        self.__write_log()
        self.state = 'discard-pick'
        self.wait_action = len(self.pairing_card) == 2
        
        return self.state if self.silence else self.__call__()
    
    def discard_pick(self,card=None):
        assert self.state == 'discard-pick'
        assert (card in self.pairing_card) if self.wait_action else (card == None)
        # action
        self.__collect_card(card)
        # next state
        self.__write_log()
        self.state = 'draw'
        self.wait_action = False
        
        return self.state if self.silence else self.__call__()
        
    
        
        
        
        
        
        
        
        
        
        