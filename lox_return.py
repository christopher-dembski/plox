class Return(Exception):
    def __init__(self, value):
        super()
        self.value = value
