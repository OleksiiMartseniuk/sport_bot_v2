import enum


class Week(enum.Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


WeekDict = {
    0: "Понедельник",
    1: "Вторник",
    2: "Середа",
    3: "Четверг",
    4: "Пятница",
    5: "Суббота",
    6: "Воскресение",
}
