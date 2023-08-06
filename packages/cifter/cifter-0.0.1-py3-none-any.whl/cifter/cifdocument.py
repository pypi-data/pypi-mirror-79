class CIFDocument:

    def __init__(self):
        self.schedule_records = []

    def add_schedule_record(self, record):
        self.schedule_records.append(record)