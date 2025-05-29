from collections import deque, defaultdict
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from ..model.Logs import Logs


class Cache:
    def __init__(self, ):
        self.logs: deque[Logs] = deque() ## mantiene los logs en orden de llegada para eliminar los viejos.
        self.by_sala: Dict[str, List[Logs]] = defaultdict(list)
        self.by_timestamp: Dict[datetime, Logs] = {}

    def _clean_old_logs(self):
        now = datetime.now()
        five_minutes_ago = now - timedelta(minutes=5)
        extracted = []

        while self.logs and self.logs[0].timestamp < five_minutes_ago:
            old_log = self.logs.popleft()
            self.by_sala[old_log.sala].remove(old_log)
            self.by_timestamp.pop(old_log.timestamp, None)
            extracted.append(old_log)
        
        return extracted

    def add_log(self, log: Logs):
        self._clean_old_logs()

        self.logs.append(log)
        self.by_sala[log.sala].append(log)
        self.by_timestamp[log.timestamp] = log

    def get_logs_by_sala(self, sala: str) -> List[Logs]:
        self._clean_old_logs()
        return list(self.by_sala.get(sala, []))

    def get_log_by_timestamp(self, timestamp: datetime) -> Optional[Logs]:
        self._clean_old_logs()
        return self.by_timestamp.get(timestamp)