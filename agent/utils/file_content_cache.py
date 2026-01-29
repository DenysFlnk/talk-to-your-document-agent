import threading
from datetime import datetime, time, timedelta
from typing import Tuple


class FileContentCache:
    def __init__(self):
        self._cache: dict[str, Tuple[str, datetime]] = {}
        self._lock = threading.Lock()
        self._cleanup_thread = None
        self._stop_event = threading.Event()
        self._running = False

    @classmethod
    def create(cls) -> "FileContentCache":
        instance = cls()
        instance.start_cleanup_task()
        return instance

    def get(self, key: str) -> str | None:
        with self._lock:
            if key in self._cache:
                content, timestamp = self._cache[key]
                if datetime.now() - timestamp < timedelta(hours=24):
                    return content
                else:
                    del self._cache[key]
            return None

    def set(self, key: str, content: str) -> None:
        with self._lock:
            self._cache[key] = (content, datetime.now())

    def clear(self) -> None:
        with self._lock:
            self._cache.clear()

    def cleanup_old_entries(self) -> int:
        now = datetime.now()
        cutoff_time = now - timedelta(hours=24)

        with self._lock:
            keys_to_remove = [
                key
                for key, (_, timestamp) in self._cache.items()
                if timestamp < cutoff_time
            ]

            for key in keys_to_remove:
                del self._cache[key]

            removed_count = len(keys_to_remove)
            if removed_count > 0:
                print(
                    f"[FileContentCache] Cleaned up {removed_count} expired entries at {now}"
                )

            return removed_count

    def _schedule_midnight_cleanup(self) -> None:
        while not self._stop_event.is_set():
            now = datetime.now()
            tomorrow = now + timedelta(days=1)
            midnight = datetime.combine(tomorrow.date(), time.min)
            seconds_until_midnight = (midnight - now).total_seconds()

            if self._stop_event.wait(timeout=seconds_until_midnight):
                break

            if not self._stop_event.is_set():
                self.cleanup_old_entries()

    def start_cleanup_task(self) -> None:
        if not self._running:
            self._running = True
            self._stop_event.clear()
            self._cleanup_thread = threading.Thread(
                target=self._schedule_midnight_cleanup,
                daemon=True,
                name="FileContentCache-Cleanup",
            )
            self._cleanup_thread.start()
            print(
                "[FileContentCache] Started automatic cleanup thread (runs at midnight)"
            )

    def stop_cleanup_task(self) -> None:
        if self._running:
            self._running = False
            self._stop_event.set()
            if self._cleanup_thread and self._cleanup_thread.is_alive():
                self._cleanup_thread.join(timeout=5)
            print("[FileContentCache] Stopped automatic cleanup thread")

    def size(self) -> int:
        with self._lock:
            return len(self._cache)

    def __contains__(self, key: str) -> bool:
        return self.get(key) is not None
