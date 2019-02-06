class Stock(object):
    def __init__(self, name='', bankuai='', shijinglv=''):
        self.name = name
        self.bankuai = bankuai
        self.shijinglv = shijinglv
    def output(self):
        print(self.bankuai, self.name, self.shijinglv)
    def SJL(self):
        return self.shijinglv