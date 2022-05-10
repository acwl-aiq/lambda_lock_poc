# This is a dummy file to check test coverage T

class Dummy:
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
