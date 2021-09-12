from vacuum import VacuumAgent
import random
import time

class DmeyersVacuumAgent(VacuumAgent):

    def __init__(self):
        super().__init__()
        self.last_per = None
        self.chances = [25, 50, 75 ,100]
        self.num = 0
        self.robot_pin = [0,0]
        self.save_data = None
        self.last_pos = [0,0]
        self.bump = 0
        self.steps = 0
        self.xp = 0
        self.once = False
        self.last_move = None


    def program(self, percept):
        if self.save_data == None:
            self.save_data = [["0R"]]  



        
        ran = random.uniform(0,sum(self.chances))
        
        if percept[0] == "Dirty":
            self.xp = self.xp - 10
            self.xp = self.xp + 80
            return "Suck"
        if self.steps > 300 and self.xp < 2000 and self.once == False:
            self.once = True


        if self.steps > 450:
            return "NoOp"

        self.change_chances()
        if percept[1] == "Bump":
            self.bump = self.bump + 1

            self.save_data[self.robot_pin[0]][self.robot_pin[1]] =  200


            self.robot_pin = self.last_pos.copy()

   
        self.bulid_map(ran)
        nice = 0
        while self.save_data[self.robot_pin[0]][self.robot_pin[1]] == 200:
            
            nice = nice +1
            if nice == 100:
                self.chances = [25, 50, 75 ,100]
                

            self.robot_pin = self.last_pos.copy()
            ran = random.uniform(0,sum(self.chances))
            self.bulid_map(ran)
        times = ""
        if self.save_data[self.robot_pin[0]][self.robot_pin[1]] != 150:
            times = self.save_data[self.robot_pin[0]][self.robot_pin[1]] // 4
        
        self.save_data[self.robot_pin[0]][self.robot_pin[1]] = "{}R".format(times)


        self.last_per = self.random_choice(ran)
        self.steps =  self.steps + 1
        self.xp = self.xp -3
        return self.random_choice(ran)
    
    def random_choice(self,num):
        if num< self.chances[0]:
            return "Left"
        elif num < self.chances[1] + self.chances[0]:
            return "Right"
        elif num < self.chances[2] + self.chances[1] + self.chances[0]:
            return "Up"
        else:
            return "Down"

    def change_chances(self):
        up_total = 0
        blank_up_total = 0
        for i in range(0, self.robot_pin[0] ):
            for l in range(len(self.save_data[0])):
                if self.save_data[i][l] == 0:
                    blank_up_total = blank_up_total + 1
                up_total = up_total + self.save_data[i][l]

        down_total = 0
        blank_down_total = 0

        for i in range(self.robot_pin[0]+1, len(self.save_data)):
            for l in range(len(self.save_data[0])):
                if self.save_data[i][l] == 0:
                    blank_down_total = blank_down_total + 1

                down_total = down_total + self.save_data[i][l]
        blank_left_total = 0

        left_total = 0
        for i in range(0, len(self.save_data)):
            for l in range(0,self.robot_pin[1]):
                if self.save_data[i][l] == 0:
                    blank_left_total = blank_left_total + 1
                
                left_total = left_total + self.save_data[i][l] 

        blank_right_total = 0

        right_total = 0
        for i in range(0, len(self.save_data)):
            for l in range(self.robot_pin[1] + 1,len(self.save_data[0])):
                if self.save_data[i][l] == 0:
                    blank_right_total = blank_right_total + 1
                right_total = right_total + self.save_data[i][l]  




        close_left_total =0
        close_right_total=0
        close_up_total = 0
        close_down_total = 0
        if len(self.save_data) >self.robot_pin[0] + 1:
            close_down_total = self.save_data[self.robot_pin[0] + 1][self.robot_pin[1]]
        if -1 <self.robot_pin[0] - 1:
            close_up_total = self.save_data[self.robot_pin[0] - 1][self.robot_pin[1]]
        if len(self.save_data[0]) >self.robot_pin[1] + 1:
            close_right_total = self.save_data[self.robot_pin[0] ][self.robot_pin[1] + 1]
        if -1 <self.robot_pin[1] - 1:
            close_left_total = self.save_data[self.robot_pin[0]][self.robot_pin[1] - 1]
        close_total = close_left_total + close_right_total + close_up_total+ close_down_total
        
        if close_total>0:
            norm_close_up_total = close_up_total/close_total
            norm_close_down_total = close_down_total/close_total       
            norm_close_left_total = close_left_total/close_total
            norm_close_right_total = close_right_total/close_total     

            close_left = 1000 - (1000*norm_close_left_total)
            close_right = (1000- (1000*norm_close_right_total))
            close_up = (1000-(1000*norm_close_up_total))
            close_down = (1000- (1000*norm_close_down_total))
            

        
        blank_total = blank_up_total + blank_down_total + blank_left_total + blank_right_total
        blank_left = 0
        blank_right = 0
        blank_up = 0
        blank_down =0
        if blank_total >0:
            norm_blank_up_total = blank_up_total/blank_total
            norm_blank_down_total = blank_down_total/blank_total       
            norm_blank_left_total = blank_left_total/blank_total
            norm_blank_right_total = blank_right_total/blank_total  
            
            blank_left = 1000*norm_blank_left_total
            blank_right = 1000*norm_blank_right_total
            blank_up = 1000*norm_blank_up_total
            blank_down = 1000*norm_blank_down_total
        

        total = up_total + down_total + left_total + right_total
        if total >0:
            norm_up_total = up_total/total
            norm_down_total = down_total/total       
            norm_left_total = left_total/total
            norm_right_total = right_total/total     


            left = 1000 - (1000*norm_left_total)
            right = (1000- (1000*norm_right_total))
            up = (1000-(1000*norm_up_total))
            down = (1000- (1000*norm_down_total))
            self.chances[0] = left +blank_left + close_left

            self.chances[1] = right + blank_right +close_right

            self.chances[2] = up +blank_up +close_up
        
            self.chances[3] = down + blank_down  +close_down

        if total>0 and blank_total >0:
            self.chances[0] = left +blank_left
            self.chances[1] = right + blank_right
            self.chances[2] = up +blank_up
            self.chances[3] = down + blank_down

            
        if self.last_per == "Down":
            self.chances[2] = 0
        elif self.last_per == "Right":
            self.chances[0] = 0
        elif self.last_per == "Up":
            self.chances[3] = 0
        elif self.last_per == "Left":
            self.chances[1] = 0



        
 
    def bulid_map(self,ran):
        if self.random_choice(ran) == "Left":
            if isinstance(self.save_data[self.robot_pin[0]][self.robot_pin[1]], str):
                mult = self.save_data[self.robot_pin[0]][self.robot_pin[1]][0:-1]

                self.save_data[self.robot_pin[0]][self.robot_pin[1]] =  4 * (3*(int(mult) +1))
            
            if self.robot_pin[1] == 0:
                col = len(self.save_data[0])+ 1
                row = len(self.save_data)
                arr = [[0]*col for _ in range(row)]


                for i in range(len(self.save_data)):
                    for l in range(len(self.save_data[i])):
                        arr[i][l+1] = self.save_data[i][l]

                self.save_data = arr
                self.robot_pin[1] = self.robot_pin[1] + 1
                self.last_pos = self.robot_pin.copy()
                self.robot_pin[1] = 0
                


            else:
                self.last_pos = self.robot_pin.copy()
                self.robot_pin[1] = self.robot_pin[1] - 1


        elif self.random_choice(ran) == "Right":
            if isinstance(self.save_data[self.robot_pin[0]][self.robot_pin[1]], str):
                mult = self.save_data[self.robot_pin[0]][self.robot_pin[1]][0:-1]
                self.save_data[self.robot_pin[0]][self.robot_pin[1]] =  4 * (3*(int(mult) +1))

            if self.robot_pin[1]+1 == len(self.save_data[0]):
                col = len(self.save_data[0])+ 1
                row = len(self.save_data)
                arr = [[0]*col for _ in range(row)]

                for i in range(len(self.save_data)):
                    for l in range(len(self.save_data[i])):
                        arr[i][l] = self.save_data[i][l]

                self.save_data = arr

            self.last_pos = self.robot_pin.copy()
            self.robot_pin[1] = self.robot_pin[1] + 1

        elif self.random_choice(ran) == "Up":
            if isinstance(self.save_data[self.robot_pin[0]][self.robot_pin[1]], str):
                mult = self.save_data[self.robot_pin[0]][self.robot_pin[1]][0:-1]
                self.save_data[self.robot_pin[0]][self.robot_pin[1]] =  4 * (3*(int(mult) +1))

            if self.robot_pin[0] == 0:
                col = len((self.save_data[0]))
                row = len(self.save_data) + 1
                arr = [[0]*col for _ in range(row)]

                for i in range(len(self.save_data)):
                    for l in range(len(self.save_data[i])):
                        arr[i+1][l] = self.save_data[i][l]

                self.save_data = arr
                self.robot_pin[0] = self.robot_pin[0] + 1
                self.last_pos = self.robot_pin.copy()
                self.robot_pin[0] = 0
                

            else:
                self.last_pos = self.robot_pin.copy()
                self.robot_pin[0] = self.robot_pin[0] - 1


        elif self.random_choice(ran) == "Down":

            if isinstance(self.save_data[self.robot_pin[0]][self.robot_pin[1]], str):
                mult = self.save_data[self.robot_pin[0]][self.robot_pin[1]][0:-1]
                self.save_data[self.robot_pin[0]][self.robot_pin[1]] =  4 * (3*(int(mult) +1))
            if self.robot_pin[0]+1 == len(self.save_data):
                col = len(self.save_data[0])
                row = len(self.save_data) + 1
                arr = [[0]*col for _ in range(row)]

                for i in range(len(self.save_data)):
                    for l in range(len(self.save_data[i])):
                        arr[i][l] = self.save_data[i][l]

                self.save_data = arr

            self.last_pos = self.robot_pin.copy()
            self.robot_pin[0] = self.robot_pin[0] + 1
        


