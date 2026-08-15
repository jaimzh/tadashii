"""Run a small, repeatable end-to-end recommendation benchmark."""

import argparse
from pathlib import Path
import sys
from time import perf_counter

BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BACKEND_DIR))

from app.api.recommend import recommend
from app.models.schema import RecommendRequest


PROMPTS = [
    "Recommend a dark psychological thriller like Death Note",
    "I want a wholesome relaxing slice-of-life anime",
    "An emotional lonely underdog who grows stronger and finds real friends",
    "Surprise me with an obscure science-fiction mystery from the 2000s",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--prompt-index",
        type=int,
        choices=range(1, len(PROMPTS) + 1),
        help="Run only the selected one-based prompt index.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    indexed_prompts = list(enumerate(PROMPTS, start=1))

    if args.prompt_index is not None:
        indexed_prompts = [indexed_prompts[args.prompt_index - 1]]

    suite_started_at = perf_counter()

    for index, prompt in indexed_prompts:
        started_at = perf_counter()
        print(f"BENCHMARK_START {index}: {prompt}", flush=True)

        try:
            response = recommend(RecommendRequest(prompt=prompt))
        except Exception as exc:
            duration = perf_counter() - started_at
            print(
                f"BENCHMARK_ERROR {index}: duration_s={duration:.3f} "
                f"error={type(exc).__name__}: {exc}",
                flush=True,
            )
            continue

        duration = perf_counter() - started_at
        print(
            f"BENCHMARK_DONE {index}: duration_s={duration:.3f} "
            f"results={len(response['results'])}",
            flush=True,
        )

    suite_duration = perf_counter() - suite_started_at
    print(f"BENCHMARK_SUITE_DONE duration_s={suite_duration:.3f}", flush=True)


if __name__ == "__main__":
    main()
