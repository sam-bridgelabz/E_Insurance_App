from enum import Enum


class DepartmentEnum(str, Enum):
    OPERATIONS = "operations"
    HR = "hr"
    FINANCE = "finance"
    TECH = "tech"
