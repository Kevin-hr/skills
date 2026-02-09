# -*- coding: utf-8 -*-
"""
Account Niche Filter - Filter hotspots based on account profile
"""

import sys
import os

# Set UTF-8 encoding for Windows
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import json
import re
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict

# Path config - use HOME directory for user profiles
if sys.platform == 'win32':
    USER_DIR = Path(os.environ.get('USERPROFILE', Path.home()))
else:
    USER_DIR = Path.home()

CONFIG_DIR = USER_DIR / ".agent" / "account-profiles"


@dataclass
class Profile:
    """Account profile config"""
    name: str
    description: str
    target_audience: Dict
    content_rules: Dict
    script_preference: Dict
    keywords: Dict

    def to_dict(self) -> dict:
        return asdict(self)


class AccountNicheFilter:
    """Account niche filter"""

    def __init__(self, profile_name: Optional[str] = None):
        self.profiles = self._load_all_profiles()
        self.current_profile = self._get_profile(profile_name)

    def _load_all_profiles(self) -> Dict[str, Profile]:
        profiles = {}
        config_dir = CONFIG_DIR

        if not config_dir.exists():
            config_dir.mkdir(parents=True, exist_ok=True)
            default_profile = self._create_default_profile()
            profiles["default"] = default_profile
            self._save_profile(default_profile, config_dir / "default.json")
            return profiles

        for file_path in config_dir.glob("*.json"):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    profile = Profile(**data)
                    profiles[profile.name] = profile
            except Exception as e:
                print(f"[WARN] Failed to load {file_path}: {e}")

        if not profiles:
            default_profile = self._create_default_profile()
            profiles["default"] = default_profile

        return profiles

    def _get_profile(self, profile_name: Optional[str] = None) -> Profile:
        if profile_name is None:
            profile_name = "default"

        if profile_name in self.profiles:
            return self.profiles[profile_name]

        if self.profiles:
            return list(self.profiles.values())[0]

        return self._create_default_profile()

    def _create_default_profile(self) -> Profile:
        return Profile(
            name="default",
            description="Default account profile",
            target_audience={
                "age_ranges": ["25-35"],
                "interests": ["职场", "成长", "赚钱"]
            },
            content_rules={
                "forbidden_topics": [],
                "preferred_emotions": []
            },
            script_preference={
                "types": ["演绎向"]
            },
            keywords={
                "core": ["职场", "赚钱"],
                "long_tail": [],
                "triggers": []
            }
        )

    def _save_profile(self, profile: Profile, file_path: Path):
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(profile.to_dict(), f, ensure_ascii=False, indent=2)

    def _extract_keywords(self, text: str) -> List[str]:
        stopwords = {"的", "了", "是", "在", "和", "与", "及", "或", "等", "这", "那", "有", "没", "不"}
        words = re.findall(r'[\w\u4e00-\u9fff]+', text)
        return [w for w in words if w not in stopwords and len(w) > 1]

    def _calculate_keyword_match(self, keywords: List[str], profile: Profile) -> float:
        core_kws = profile.keywords.get("core", [])
        long_tail_kws = profile.keywords.get("long_tail", [])
        trigger_kws = profile.keywords.get("triggers", [])

        if not core_kws:
            return 0.5

        text = " ".join(keywords).lower()
        score = 0.0

        # Core keywords - highest weight
        for kw in core_kws:
            if kw.lower() in text:
                score += 0.3  # Each core keyword gives 0.3

        # Long tail keywords - medium weight
        for kw in long_tail_kws:
            if kw.lower() in text:
                score += 0.1  # Each long tail keyword gives 0.1

        # Trigger words - bonus weight
        for kw in trigger_kws:
            if kw.lower() in text:
                score += 0.15  # Each trigger gives 0.15

        # Cap at 1.0
        return min(score, 1.0)

    def _check_forbidden(self, keywords: List[str], profile: Profile) -> bool:
        forbidden = profile.content_rules.get("forbidden_topics", [])
        if not forbidden:
            return False
        text = " ".join(keywords)
        return any(kw in text for kw in forbidden)

    def score_hotspot(self, hotspot: Dict) -> Dict:
        topic = hotspot.get("topic", "")
        keywords = self._extract_keywords(topic)

        # Forbidden check
        if self._check_forbidden(keywords, self.current_profile):
            return {
                "topic": topic,
                "passed": False,
                "score": 0,
                "reasons": ["Contains forbidden topic"],
                "recommended_script": None,
                "match_details": {"keyword_score": 0}
            }

        # Keyword match
        keyword_score = self._calculate_keyword_match(keywords, self.current_profile)

        # Heat boost
        heat = hotspot.get("heat", 0)
        heat_boost = min(heat / 1000000, 0.2)
        final_score = min(keyword_score + heat_boost, 1.0)

        passed = final_score >= 0.5
        recommended = self._recommend_script_type(keywords) if passed else None

        return {
            "topic": topic,
            "passed": passed,
            "score": round(final_score, 3),
            "reasons": ["Keyword match" if keyword_score > 0.3 else ""],
            "recommended_script": recommended,
            "match_details": {
                "keyword_score": round(keyword_score, 3),
                "heat_boost": round(heat_boost, 3)
            }
        }

    def _recommend_script_type(self, keywords: List[str]) -> str:
        types = self.current_profile.script_preference.get("types", ["演绎向"])
        return types[0] if types else "演绎向"

    def filter_hotspots(self, hotspots: List[Dict], max_results: int = 5) -> Dict:
        results = []
        passed_count = 0

        for hotspot in hotspots:
            scored = self.score_hotspot(hotspot)
            if scored["passed"]:
                passed_count += 1
                results.append(scored)

        results.sort(key=lambda x: x["score"], reverse=True)
        results = results[:max_results]

        return {
            "profile": self.current_profile.name,
            "total_input": len(hotspots),
            "passed_count": passed_count,
            "returned_count": len(results),
            "results": results
        }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Account Niche Filter")
    parser.add_argument("--hotspots", "-i", help="Hotspots JSON file")
    parser.add_argument("--profile", "-p", help="Profile name")
    parser.add_argument("--max", "-m", type=int, default=5, help="Max results")
    parser.add_argument("--list", "-l", action="store_true", help="List profiles")
    args = parser.parse_args()

    if args.list:
        print("\nAvailable profiles:")
        for name in AccountNicheFilter().profiles.keys():
            print(f"  - {name}")
        return

    filter = AccountNicheFilter(args.profile)

    if args.hotspots:
        with open(args.hotspots, "r", encoding="utf-8") as f:
            hotspots = json.load(f)
        results = filter.filter_hotspots(hotspots, args.max)
    else:
        test_hotspots = [
            {"topic": "职场新人必备技能", "heat": 500000, "platform": "douyin"},
            {"topic": "明星恋情曝光", "heat": 800000, "platform": "weibo"},
            {"topic": "副业赚钱方法", "heat": 300000, "platform": "douyin"},
        ]
        results = filter.filter_hotspots(test_hotspots, args.max)
        print(f"\nUsing profile: {filter.current_profile.name}")
        print("-" * 50)

    print(f"\nResults: {results['passed_count']}/{results['total_input']} passed")
    print("-" * 50)

    for item in results["results"]:
        status = "[PASS]" if item["passed"] else "[FAIL]"
        print(f"{status} {item['topic']}")
        print(f"  Score: {item['score']} | Script: {item['recommended_script']}")


if __name__ == "__main__":
    main()
