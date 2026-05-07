"""Run `toolkit run all` + `toolkit validate all` for each support dataset.

Usage:
    python scripts/run_support_datasets.py --support-json <path>

The support JSON file should contain a list of dicts with keys:
    - config (str): path to the dataset.yml
    - years (list[int]): years to run
    - name (str, optional): display name
"""

import json
import subprocess
import sys


def main() -> None:
    if len(sys.argv) != 3 or sys.argv[1] != "--support-json":
        print(f"Usage: {sys.argv[0]} --support-json <path>", file=sys.stderr)
        sys.exit(1)

    support_path = sys.argv[2]
    with open(support_path) as f:
        support_list = json.load(f)

    for entry in support_list:
        config = entry["config"]
        years = entry.get("years", [])
        name = entry.get("name", config)
        print(f"::notice::Running support dataset: {name} ({config})")
        log_tag = config.replace("/", "_").replace(".", "_")

        for year in years:
            print(f"::notice::Running support {config} for year {year}")
            for cmd, log_suffix in [
                (["toolkit", "run", "all", "--config", config, "--years", str(year)], "run"),
                (["toolkit", "validate", "all", "--config", config, "--years", str(year)], "validate"),
            ]:
                log_name = f"support_{log_suffix}_{log_tag}_{year}.log"
                result = subprocess.run(cmd, capture_output=True, text=True)
                with open(log_name, "w") as lf:
                    lf.write(result.stdout)
                    if result.stderr:
                        lf.write("\nSTDERR:\n" + result.stderr)
                if result.returncode != 0:
                    print(
                        f"::error::{cmd[0]} {cmd[1]} fallito per {config} "
                        f"anno {year} (exit={result.returncode})"
                    )
                    sys.exit(1)


if __name__ == "__main__":
    main()
