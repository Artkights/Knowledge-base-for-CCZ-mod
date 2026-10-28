"""Version domains shared by generators, query tools and validation.

6.5pl remains searchable as a candidate/research domain. It has no independent
verified profile and deliberately does not have a structured-data root.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VERSIONS = ("6.4", "6.5", "6.5pl", "6.6", "legacy")
DATA_VERSIONS = tuple(version for version in VERSIONS if version != "6.5pl")
PROFILE_REQUIRED_VERSIONS = frozenset({"6.4", "6.5", "6.6"})
RESEARCH_ONLY_VERSIONS = frozenset({"6.5pl"})
REFERENCE_FILES = {
    "engine-profile": "profiles.md", "function": "functions.md", "global": "globals.md",
    "data-structure": "structures.md", "file-format": "file-formats.md",
    "patch-recipe": "patches.md", "mechanism": "mechanisms.md",
    "effect-stub": "effect-stubs.md", "script-command": "script-commands.md",
    "workflow": "workflows.md", "test-contract": "test-contracts.md",
    "case-study": "case-studies.md",
}


def data_paths(root: Path = ROOT) -> list[Path]:
    return sorted(path for version in DATA_VERSIONS for path in root.glob(version + "/data/**/*.json"))
