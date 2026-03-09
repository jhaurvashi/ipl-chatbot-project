import csv
import os
from collections import defaultdict, Counter
from typing import Dict, Optional, List, Any


class DataLoadError(Exception):
    pass


class IPLAnalyticsService:
    """
    Service responsible for loading IPL data from CSV and answering analytics queries.

    Assumed CSV format (file: data/ipl_matches.csv):
    - season: int (e.g. 2016)
    - match_id: string/int
    - team1: string
    - team2: string
    - winner: string (winning team)
    - top_scorer: string (player name for this match)
    - top_scorer_runs: int (runs scored by top_scorer in this match)
    """

    def __init__(self, csv_path: Optional[str] = None):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        default_path = os.path.join(base_dir, "data", "ipl_matches.csv")
        self.csv_path = csv_path or default_path

        self._matches: List[Dict[str, Any]] = []
        self._load_data()

    def _load_data(self) -> None:
        if not os.path.exists(self.csv_path):
            raise DataLoadError(
                f"IPL CSV dataset not found at '{self.csv_path}'. "
                f"Place your IPL matches CSV there or pass a path explicitly."
            )

        matches: List[Dict[str, Any]] = []
        try:
            with open(self.csv_path, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Normalize and cast types safely
                    season_raw = row.get("season", "")
                    runs_raw = row.get("top_scorer_runs", "0")
                    match = {
                        "season": int(season_raw) if season_raw else None,
                        "match_id": row.get("match_id"),
                        "team1": row.get("team1"),
                        "team2": row.get("team2"),
                        "winner": row.get("winner"),
                        "top_scorer": row.get("top_scorer"),
                        "top_scorer_runs": int(runs_raw) if runs_raw else 0,
                    }
                    matches.append(match)
        except Exception as exc:
            raise DataLoadError(f"Failed to load IPL data: {exc}") from exc

        self._matches = matches

    def get_overall_top_scorer(self) -> Optional[Dict[str, Any]]:
        if not self._matches:
            return None

        runs_by_player: defaultdict = defaultdict(int)
        for m in self._matches:
            player = m.get("top_scorer")
            runs = m.get("top_scorer_runs") or 0
            if player:
                runs_by_player[player] += runs

        if not runs_by_player:
            return None

        top_player, top_runs = max(runs_by_player.items(), key=lambda x: x[1])
        return {"player": top_player, "total_runs": top_runs}

    def get_winner_by_year(self, year: int) -> Optional[Dict[str, Any]]:
        if not self._matches:
            return None

        winners = [m.get("winner") for m in self._matches if m.get("season") == year and m.get("winner")]
        if not winners:
            return None

        counts = Counter(winners)
        team, wins = max(counts.items(), key=lambda x: x[1])
        return {"year": year, "team": team, "wins": wins}

