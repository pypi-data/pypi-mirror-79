from .errors import CIFParseError
from .cifdocument import CIFDocument
from .train_schedule import TrainSchedule


def handle_bad_lines(func):
    def _inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            raise CIFParseError("Line was too short")
    return _inner


def record_type(line) -> str:
    try:
        return line[0:2]
    except IndexError:
        raise CIFParseError("Line too short")


def is_comment(line) -> bool:
    try:
        return line[0] == "/"
    except IndexError:
        raise CIFParseError("Unexpected empty line")


def is_schedule_record(line) -> bool:
    return record_type(line) in ["BS", "LO", "LI", "LT", "BX"]


def _expect_header(self, line):
    pass


@handle_bad_lines
def parse_basic_schedule_record(line):
    return {
        'type': line[0:2],
        'transaction_type': line[2:3],
        'train_uid'		: line[3:9],
        'start_date'	: line[9:15],
        'end_date'		: line[15:21],
        'days_run'		: line[21:28],
        'bank_holiday_running'	: line[28:29],
        'train_status'	: line[29:30],
        'train_category': line[30:32],
        'train_identity': line[32:36],
        'headcode'		: line[36:40],
        'train_service_code'	: line[41:49],
        'portion_id'	: line[49:50],
        'power_type'	: line[50:53],
        'timing_load'	: line[53:57],
        'speed'			: line[57:60],
        'operating_characteristics'	: line[60:66],
        'train_class'	: line[66:67],
        'sleepers'		: line[67:68],
        'reservations'	: line[68:69],
        'catering_code'	: line[70:74],
        'service_branding'	: line[74:78],
        'stp_indicator'	: line[79:80]
    }


@handle_bad_lines
def parse_origin_location_record(line):
    return {
        'type'				: line[0:2],
        'tiploc_code'		: line[2:9],
        'tiploc_instance'	: line[9:10],
        'departure'			: line[10:15],
        'public_departure'	: line[15:19],
        'platform'			: line[19:22],
        'line'				: line[22:25],
        'engineering_allowance'	: line[25:27],
        'pathing_allowance'	: line[27:29],
        'activity'			: line[29:41],
        'performance_allowance'	: line[41:43]
    }


@handle_bad_lines
def parse_intermediate_location_record(line):
    return {
        'type'				: line[0:2],
        'tiploc_code'		: line[2:9],
        'tiploc_instance'	: line[9:10],
        'arrival'			: line[10:15],
        'departure'			: line[15:20],
        'pass'				: line[20:25],
        'public_arrival'	: line[25:29],
        'public_departure'	: line[29:33],
        'platform'			: line[33:36],
        'line'				: line[36:39],
        'path'				: line[39:42],
        'activity'			: line[42:54],
        'engineering_allowance'	: line[54:56],
        'pathing_allowance'	: line[56:58],
        'performance_allowance'	: line[58:60]
    }


@handle_bad_lines
def parse_terminating_location_record(line):
    return {
        'type'				: line[0:2],
        'tiploc_code'		: line[2:9],
        'tiploc_instance'	: line[9:10],
        'arrival'			: line[10:15],
        'public_arrival'	: line[15:19],
        'platform'			: line[19:22],
        'path'				: line[22:25],
        'activity'			: line[25:37]
    }


def parse_line(line):
    record_actions = {
        "BS": parse_basic_schedule_record,
        "LO": parse_origin_location_record,
        "LI": parse_intermediate_location_record,
        "LT": parse_terminating_location_record
    }
    try:
        return record_actions[record_type(line)](line)
    except KeyError:
        return None


def parse_itterable(cif_content) -> CIFDocument:
    # Parse an itterable where each entry is a line of the CIF file
    current_schedule_record = None
    line_no = 0
    document = CIFDocument()
    for line in cif_content:
        line_no += 1
        try:
            if is_comment(line):
                continue
            line_record = parse_line(line)
            if line_record is None:
                # Not a record we handle yet
                continue

            if is_schedule_record(line):
                if current_schedule_record is None:
                    current_schedule_record = TrainSchedule(line_record)
                    document.add_schedule_record(current_schedule_record)
                else:
                    current_schedule_record.add_record(line_record)
                    if current_schedule_record.is_complete():
                        current_schedule_record = None
            else:
                current_schedule_record = None
                # Nothing happens with these just yet
        except CIFParseError as e:
            raise CIFParseError(f"{str(e)} on line {line_no}")
    return document
