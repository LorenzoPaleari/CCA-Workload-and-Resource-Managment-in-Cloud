from datetime import datetime
from enum import Enum
import urllib.parse


LOG_STRING = "{timestamp} {event} {job_name} {args}"

class Job(Enum):
    SCHEDULER = "scheduler"
    MEMCACHED = "memcached"
    BLACKSCHOLES = "blackscholes"
    CANNEAL = "canneal"
    DEDUP = "dedup"
    FERRET = "ferret"
    FREQMINE = "freqmine"
    RADIX = "radix"
    VIPS = "vips"


class SchedulerLogger:
    def __init__(self):
        start_date = datetime.now().strftime("%Y%m%d_%H%M%S")

        self.file = open(f"log/log{start_date}.txt", "w")
        self._log("start", "scheduler")

    def _log(self, event: str, job_name: str, args: str = "") -> None:
        self.file.write(
            LOG_STRING.format(timestamp=datetime.now().isoformat(), event=event, job_name=job_name,
                              args=args).strip() + "\n")
        self.file.flush()

    def job_start(self, job:str, initial_cores: list, initial_threads: int) -> None:
        assert job != "scheduler", "You don't have to log SCHEDULER here"

        self._log("start", job, "[" + str(initial_cores) + "]" + " " +str(initial_threads))


    def job_end(self, job: str) -> None:
        assert job != Job.SCHEDULER, "You don't have to log SCHEDULER here"

        self._log("end", job)


    def update_cores(self, job: str, cores: list) -> None:
        assert job != Job.SCHEDULER, "You don't have to log SCHEDULER here"

        self._log("update_cores", job, "["+(",".join(str(i) for i in cores))+"]")


    def job_pause(self, job: str) -> None:
        assert job != "scheduler", "You don't have to log SCHEDULER here"

        self._log("pause", job)


    def job_unpause(self, job: str) -> None:
        assert job != "scheduler", "You don't have to log SCHEDULER here"

        self._log("unpause", job)


    def custom_event(self, job:str, comment: str):
        self._log("MESSAGE - ", job, comment)


    def end(self) -> None:
        self._log("end", "scheduler")
        self.file.flush()
        self.file.close()
