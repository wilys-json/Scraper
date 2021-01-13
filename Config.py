class Config:
    def __init__(self, **kwargs):
        if kwargs:
            for attrb, val in kwargs.items():
                self.__dict__[attrb] = val
