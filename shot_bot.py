import numpy as np
# import field as fd


class GetCoordinates:

    def __init__(self):
        self.shot = np.arange(0, 100)
        # print(self.shot)

    def creatShotCoordinates(self):
        idx = np.random.randint(len(self.shot))
        random_choices = self.shot[idx]
        self.shot = np.delete(self.shot, idx)

        print(random_choices)
        row = random_choices // 10
        culom = (random_choices % 10)
        print( row , culom)
        print(self.shot)





sh = GetCoordinates()
sh.creatShotCoordinates()
