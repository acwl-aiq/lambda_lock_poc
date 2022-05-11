# This is a dummy file to check test coverage T

class Dummy:

    def __init__(self):
        print("x")

    def m_dummy(self, input: bool, input2: bool, input3: bool):
        if input:
            return 3
        if input2:
            return 5

    @staticmethod
    def dummy(input: bool, input2: bool, input3: bool):
        if input2:
            return 3

        if input3:
            return 4

        if input:
            return 1
        else:
            return 2

    @staticmethod
    def dummy2(input: bool):
        if input:
            return 1
        else:
            return 2

    @staticmethod
    def dummy3(input: bool):
        if input:
            return 1
        else:
            return 2
