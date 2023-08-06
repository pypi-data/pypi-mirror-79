# cifter
Python3 ATOC CIF file parser


# Usage

```python
from cifter import parse_file

document = parse_file('ttisf760.mca')

for schedule_record in document.schedule_records:
    print("Basic record\n")
    print(schedule_record.basic_record)
    print("Origin record\n")
    print(schedule_record.origin_record)
    print("Intermediate records\n")
    for intermediate_record in schedule_record.intermediate_records:
        print(intermediate_record)
    print("Termination record\n")
    print(schedule_record.termination_record)
```

Note that the `parse_file()` method is a blocking CPU bound operation
