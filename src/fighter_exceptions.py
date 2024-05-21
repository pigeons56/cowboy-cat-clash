class Out_Of_Left_Bound(Exception):
    def __init__(self, message="Fighter out of left screen bound."):
        self.message = message
        super().__init__(self.message)

class Out_Of_Right_Bound(Exception):
    def __init__(self, message="Fighter out of right screen bound."):
        self.message = message
        super().__init__(self.message)