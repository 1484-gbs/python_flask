import random


class HogeList:
    def execute(self, max):
        hoge_list = ["hoge" + str(i) for i in range(0, random.randint(0, max))]
        return "<div>" + "<br>".join(hoge_list) + "</div>"
