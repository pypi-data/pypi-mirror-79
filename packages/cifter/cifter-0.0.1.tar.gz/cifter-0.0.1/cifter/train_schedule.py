class TrainSchedule:

    def __init__(self, basic_record):
        self.basic_record = basic_record
        self.origin_record = None
        self.intermediate_records = []
        self.termination_record = None

    def add_record(self, record):
        transaction_type = record['type']
        if transaction_type == "LO":
            self.origin_record = record
        elif transaction_type == "LI":
            self.intermediate_records.append(record)
        elif transaction_type == "LT":
            self.termination_record = record

    def is_complete(self) -> bool:
        # Returns True if all mandatory records are present
        return self.origin_record and self.termination_record
