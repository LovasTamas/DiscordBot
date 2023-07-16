class ScheduleItem:
    def __init__(self, channel, message, time, delay):
        self.channel = channel
        self.message = message
        self.time = time
        self.delay = delay
    
    def addId(self, id):
        self.id = id
