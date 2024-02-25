# J4F - "Just For Fun", or "5-minute evening projects"
# AI-matches console game, or how to create a neural network using matchboxes without a computer ;)
# Homepage: https://github.com/greentracery/J4F
# Requirements:
# - python 3.6.x or higher
#

import shelve
import random

class MemModel:
    
    model = {}
    
    steps = []
    
    datafile = 'model.data'
    
    default_values = (1, 2, 3) 
    
    def __init__(self, n:int = 15):
        """ по умолчанию 14 элементов (нумерация с 1) """
        self.get_new_model(n)
    
    def get_new_model(self, n:int):
        """ `чистая` модель -  в каждой ячейке по одному экземпляру возможных значений """
        model = {}
        i = 1
        while i < n:
            model[i] = list(self.default_values)
            i+=1
        self.model = model
        return self.model
    
    def save_step(self, model_key, out_value):
        """ сохраняем для каждого шага входное значение, выбранное значение """
        self.steps.append((model_key, out_value))
    
    def clear_steps(self):
        """ очищаем сохраненную последовательность шагов """
        self.steps.clear()
    
    def encouragement(self):
        """ поощрение - увеличиваем в ячейках модели кол-во удачно выбранных значений """
        for step in self.steps:
            self.model[step[0]].append(step[1])
            #random.shuffle(self.model[step[0]])
        self.steps.clear()
    
    def punishment(self):
        """ наказание - удаляем последнее выбранное значение из соотв.ячейки модели. 
            если выбранных значений в ячейке нет - удаляем предыдущее выбранное значение из соотв.ячейки """
        result = False
        while result is False:
            step = self.steps.pop()
            if step[1] in self.model[step[0]]:
                self.model[step[0]].remove(step[1])
                result = True
        self.steps.clear()
    
    def choice(self, input_value):
        """ выбор выходного значения """
        if input_value not in self.model.keys():
            raise Exception ("Value out of range")
        a = len(self.model[input_value])
        if a == 0:
            return 0
        index = random.randint(0, a - 1)
        out_value = self.model[input_value][index]
        if out_value > input_value:
            out_value = input_value
        self.save_step(input_value, out_value)
        return out_value
    
    def load_state(self, state_name: str):
        """ загружаем сохраненное состояние модели из файла """
        try:
            with shelve.open(self.datafile) as model_states:
                self.model = model_states[state_name]
                return self.model
        except:
            return None
    
    def save_state(self, state_name: str):
        """ сохраняем состояние модели в файл """
        try:
            with shelve.open(self.datafile) as model_states:
                model_states[state_name] = self.model
                return True
        except:
            return False
    
    def get_states_list(self):
        """ список сохраненных состояний """
        states = []
        try:
            with shelve.open(self.datafile) as model_states:
                for key in model_states.keys():
                    states.append(key)
        except:
            pass
        return states
    
    def del_state(self, state_name: str):
        """ удаляем сохраненное состояние из файла """
        try:
            with shelve.open(self.datafile) as model_states:
                if state_name in model_states.keys():
                    del model_states[state_name]
                    return True
                else:
                    return False
        except:
            return False
