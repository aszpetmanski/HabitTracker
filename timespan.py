class TimeSpan:
    def __init__(self, span: int):
        self.span = span
    def __str__(self):
        if self.span == 1:
            return 'daily'
        elif self.span == 7:
            return 'weekly'