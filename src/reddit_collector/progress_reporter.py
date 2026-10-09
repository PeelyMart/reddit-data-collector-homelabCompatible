from __future__ import annotations

import logging
import os

import requests

logger = logging.getLogger(__name__)


class ProgressReporter:
    def __init__(self) -> None:
        self.url = os.getenv("HOMELAB_PROGRESS_URL")
        self.enabled = bool(self.url)

    def report(
        self,
        *,
        status: str,
        collected: int,
        total: int | None = None,
        pages: int = 0,
        run_id: str | None = None,
    ) -> None:
        if not self.enabled:
            return

        payload = {
            "status": status,
            "collected": collected,
            "total": total,
            "pages": pages,
            "run_id": run_id,
        }

        try:
            response = requests.post(
                self.url,
                json=payload,
                headers={
                    "Authorization": f"Bearer {self.token}"
                },
                timeout=2,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            # Remote reporting must never stop collection.
            logger.debug("Could not report homelab progress: %s", exc)
