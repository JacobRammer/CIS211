"""
Jacob Rammer

Provides Appt and Agenda classes
"""
from datetime import datetime

if __name__ == "__main__":
    print("Running usage example")


class Appt:
    """
    Appointment has a start time, end time, and title
    Usage example:
        appt1 = Appt(datetime(2018, 3, 15, 13, 30), datetime(2018, 3, 15, 15, 30), "Early afternoon nap")
        appt2 = Appt(datetime(2018, 3, 15, 15, 00), datetime(2018, 3, 15, 16, 00), "Coffee break")
        if appt2 > appt1:
            print(f"appt1 '{appt1}' was over when appt2 '{appt2}'  started")
        elif appt1.overlaps(appt2):
            print("Oh no, a conflict in the schedule!")
            print(appt1.intersect(appt2))
    Should print:
        Oh no, a conflict in the schedule!
        2018-03-15 15:00 15:30 | Early afternoon nap and Coffee break
    """

    def __init__(self, start: datetime, finish: datetime, desc: str):
        """An appointment from start time to end time with a descriptions, desc.
        Start and finish should be the time of day.
        """
        assert finish > start, f"Period finish ({finish}) must be after start ({start})"
        self.start = start
        self.finish = finish
        self.desc = desc

    def __eq__(self, other: "Appt") -> bool:  # equality
        """Equality means same time period, ignoring description"""

        return self.start == other.start and self.finish == other.finish

    def __lt__(self, other: "Appt") -> bool:  # less than
        """Check to see if appointment occurs before"""

        return self.finish < other.finish

    def __gt__(self, other: "Appt") -> bool:  # greater than
        """Check to see if appointment occurs after each other"""

        return self.start > other.start

    def __str__(self) -> str:
        """The textual format of an appointment is yyyy-mm-dd:mm hh:mm | description
        Note: that this is accurate only if start and finish are on the same day
        """

        date_iso = self.start.date().isoformat()
        start_iso = self.start.time().isoformat(timespec='minutes')
        finish_iso = self.finish.time().isoformat(timespec='minutes')

        return f"{date_iso} {start_iso} {finish_iso} | {self.desc}"

    def overlaps(self, other: "Appt") -> bool:
        """Is there a non-zero overlap between these two periods? ie: app1 ends after app2 starts"""

        return self.finish.__gt__(other.start)

    def intersect(self, other: "Appt") -> "Appt":
        """Calculate the overlap time between two appointments if there are overlaps"""

        if self.finish < other.finish:
            return Appt(other.start, self.finish, f" | {self.desc} and {other.desc}")
        if other.finish > other.finish:
            return Appt(self.start, other.finish, f" | {self.desc} and {other.desc}")
        if other.start < self.start:
            return Appt(self.start, other.finish, f" | {self.desc} and {other.desc}")
        if other.start > self.start:
            return Appt(other.start, other.finish, f" | {other.desc} and {self.desc}")


class Agenda(list):
    """An Agenda is a collection of appointments.
    It has most of the methods of a list, such as
    'append' and iteration, and in
    addition it has a few special methods, including
    a method for finding conflicting appointments.

    Usage:
    appt1 = Appt(datetime(2018, 3, 15, 13, 30), datetime(2018, 3, 15, 15, 30), "Early afternoon nap")
    appt2 = Appt(datetime(2018, 3, 15, 15, 00), datetime(2018, 3, 15, 16, 00), "Coffee break")
    agenda = Agenda()
    agenda.append(appt1)
    agenda.append(appt2)
    if agenda.unconflicted():
        print(f"Agenda has no conflicts")
    else:
        print(f"In agenda:\n{agenda.text()}")
        print(f"Conflicts:\n {agenda.conflicts().text()}")

    Expected output:
    In agenda:
    2018-03-15 13:30 15:30 | Early afternoon nap
    2018-03-15 15:00 16:00 | Coffee break
    Conflicts:
    2018-03-15 15:00 15:30 | Early afternoon nap and Coffee break
    """

    def text(self) -> str:
        """Returns a string in the same form as we expect to find in the input file.
        Note that this is different from the __str__ method inherited from "list", which is still
        available
        """

        as_list = [str(appt) for appt in self]
        return "\n".join(as_list)

    def conflicts(self) -> "Agenda":
        """Returns the agenda consisting of the conflicts (overlaps) between this agenda and the other.
        Side effect: This agenda is sorted"""

        conflicts = Agenda()
        self.sort()

        for appt1 in range(len(self)):
            appt1_index = self[appt1]
            for appt2 in range(appt1 + 1, len(self)):
                appt2_index = self[appt2]
                if appt1_index.overlaps(appt2_index):
                    conflict = appt1_index.intersect(appt2_index)
                    conflicts.append(conflict)
                elif not appt1_index.overlaps(appt2_index):
                    break

        return conflicts

    def sort(self, key=lambda appt: appt.start, reverse=False):
        """We sort by a start time unless another sort key is given"""

        super().sort(key=key, reverse=reverse)

    def unconflicted(self) -> bool:
        """True if none of the appointments in this agenda overlap.
        Side effect: Agenda is sorted
        """

        return len(self.conflicts()) == 0
