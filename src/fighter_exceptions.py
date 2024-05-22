class Out_Of_Left_Bound(Exception):
    def __init__(self, message="Fighter out of left screen bound."):
        """
        Exception when fighter is out of screen's left bound.

        Parameters:
            message (str): Message to return with exception.
        """
        self.message = message
        super().__init__(self.message)


class Out_Of_Right_Bound(Exception):
    def __init__(self, message="Fighter out of right screen bound."):
        """
        Exception when fighter is out of screen's right bound.

        Parameters:
            message (str): Message to return with exception.
        """
        self.message = message
        super().__init__(self.message)