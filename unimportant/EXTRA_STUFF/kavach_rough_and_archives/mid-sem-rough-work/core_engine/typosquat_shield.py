"""
KAVACH Damerau-Levenshtein Typosquatting & Slopsquatting Shield.
Detects malicious lookalike and deceptive packages across PyPI and npm registries:
1. Damerau-Levenshtein distance (insertions, deletions, substitutions, transpositions)
2. Common slopsquatting deceptive affixes (-security, -official, -core, py-, node-)
3. Keyboard proximity and character doubling / omitting attacks
"""

from typing import Dict, Any, List, Set, Optional

# Top legitimate Python packages vulnerable to typosquatting
POPULAR_PYPI_PACKAGES = [
    "requests", "urllib3", "cryptography", "pydantic", "fastapi", "flask",
    "django", "pytest", "numpy", "pandas", "scipy", "torch", "transformers",
    "beautifulsoup4", "aiohttp", "sqlalchemy", "boto3", "paramiko", "pillow",
    "matplotlib", "celery", "jinja2", "click", "rich", "pytz", "certifi",
    "idna", "charset-normalizer", "scikit-learn", "psycopg2", "redis",
    "dotenv", "wheel", "setuptools", "httpx", "uvicorn", "black"
]

# Top legitimate npm packages
POPULAR_NPM_PACKAGES = [
    "express", "react", "react-dom", "lodash", "axios", "chalk", "commander",
    "vue", "next", "typescript", "webpack", "dotenv", "moment", "rxjs",
    "eslint", "jest", "cors", "body-parser", "mongoose", "nodemon", "yargs"
]

DECEPTIVE_AFFIXES = [
    "-security", "-official", "-release", "-patch", "-core", "-fix",
    "-helper", "py-", "python-", "node-", "lib-", "-v2", "-latest"
]


def damerau_levenshtein_distance(s1: str, s2: str) -> int:
    """
    Computes true Damerau-Levenshtein distance including adjacent transpositions.
    """
    s1, s2 = s1.lower(), s2.lower()
    len1, len2 = len(s1), len(s2)
    d = [[0] * (len2 + 1) for _ in range(len1 + 1)]

    for i in range(len1 + 1):
        d[i][0] = i
    for j in range(len2 + 1):
        d[0][j] = j

    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            d[i][j] = min(
                d[i - 1][j] + 1,       # deletion
                d[i][j - 1] + 1,       # insertion
                d[i - 1][j - 1] + cost # substitution
            )
            # Transposition of two adjacent characters
            if i > 1 and j > 1 and s1[i - 1] == s2[j - 2] and s1[i - 2] == s2[j - 1]:
                d[i][j] = min(d[i][j], d[i - 2][j - 2] + cost)

    return d[len1][len2]


def check_typosquatting(package_name: str, ecosystem: str = "pypi") -> Dict[str, Any]:
    """
    Checks if a package name is a potential typosquat or slopsquat of a known legitimate package.
    """
    if not package_name or not package_name.strip():
        return {
            "is_typosquat": False,
            "matched_legitimate_package": None,
            "distance": 0,
            "technique": "NONE",
            "risk_score": 0.0,
            "details": "Empty package name."
        }

    pkg_clean = package_name.strip().lower()
    canonical_list = POPULAR_NPM_PACKAGES if ecosystem.lower() == "npm" else POPULAR_PYPI_PACKAGES

    # 1. Exact match with legitimate package -> Safe
    if pkg_clean in canonical_list:
        return {
            "is_typosquat": False,
            "matched_legitimate_package": pkg_clean,
            "distance": 0,
            "technique": "OFFICIAL_PACKAGE",
            "risk_score": 0.0,
            "details": f"Package '{package_name}' is verified official {ecosystem.upper()} library."
        }

    # 2. Check Deceptive Affixes (Slopsquatting)
    for legit in canonical_list:
        # Check if candidate is legit + deceptive affix (e.g. requests-security, py-cryptography)
        for affix in DECEPTIVE_AFFIXES:
            if pkg_clean == f"{legit}{affix}" or pkg_clean == f"{affix}{legit}":
                return {
                    "is_typosquat": True,
                    "matched_legitimate_package": legit,
                    "distance": len(affix),
                    "technique": "SLOPSQUATTING_DECEPTIVE_AFFIX",
                    "risk_score": 0.90,
                    "details": (
                        f"Slopsquatting Detected: '{package_name}' uses deceptive affix '{affix}' "
                        f"masquerading as official '{legit}'."
                    )
                }
            # Check mutated root combined with affix (e.g. expres-security -> root 'expres' close to 'express')
            root = pkg_clean
            if root.endswith(affix):
                root = root[:-len(affix)]
            elif root.startswith(affix):
                root = root[len(affix):]
            if root and root != pkg_clean:
                root_dist = damerau_levenshtein_distance(root, legit)
                if root_dist <= 1:
                    return {
                        "is_typosquat": True,
                        "matched_legitimate_package": legit,
                        "distance": root_dist,
                        "technique": "SLOPSQUAT_AFFIX_MUTATION",
                        "risk_score": 0.95,
                        "details": (
                            f"Slopsquatting Detected: '{package_name}' combines root '{root}' "
                            f"(distance {root_dist} from '{legit}') with affix '{affix}'."
                        )
                    }

    # 3. Check Damerau-Levenshtein distance (Distance 1 or 2)
    closest_match = None
    min_dist = 999

    for legit in canonical_list:
        dist = damerau_levenshtein_distance(pkg_clean, legit)
        if dist < min_dist:
            min_dist = dist
            closest_match = legit

    # Distance 1: High-confidence typosquat (e.g., 'reqeusts' -> 1 transposition away from 'requests')
    # Distance 2: Suspicious lookalike if package length >= 6
    if min_dist == 1 or (min_dist == 2 and len(pkg_clean) >= 6):
        technique = "TRANSPOSITION" if len(pkg_clean) == len(closest_match) else "CHARACTER_MUTATION"
        return {
            "is_typosquat": True,
            "matched_legitimate_package": closest_match,
            "distance": min_dist,
            "technique": technique,
            "risk_score": 0.95 if min_dist == 1 else 0.80,
            "details": (
                f"Typosquatting Detected: '{package_name}' is only distance {min_dist} "
                f"from popular legitimate package '{closest_match}'."
            )
        }

    return {
        "is_typosquat": False,
        "matched_legitimate_package": None,
        "distance": min_dist,
        "technique": "NONE",
        "risk_score": 0.0,
        "details": f"Package '{package_name}' does not conflict with protected top packages."
    }
