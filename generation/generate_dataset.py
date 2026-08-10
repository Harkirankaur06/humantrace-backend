import argparse
import json
import time
import uuid
from pathlib import Path

from dotenv import load_dotenv

from .utils import load_topics, append_jsonl
from .providers.openai_provider import OpenAIProvider
from .providers.gemini_provider import GeminiProvider
from .providers.claude_provider import ClaudeProvider


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

TOPICS_DIR = PROJECT_ROOT / "topics"

RAW_AI_DIR = (
    PROJECT_ROOT
    / "datasets"
    / "raw"
    / "ai"
)


# Original master topic file
MASTER_TOPIC_FILE = TOPICS_DIR / "topics.txt"


# ============================================================
# PROVIDERS
# ============================================================

PROVIDERS = {

    "openai": {
        "class": OpenAIProvider,
        "topic_file": "gpt_topics.txt",
        "output_file": "gpt4o.jsonl",
        "model": "gpt-4o",
    },

    "gemini": {
        "class": GeminiProvider,
        "topic_file": "gemini_topics.txt",
        "output_file": "gemini.jsonl",
        "model": "gemini-2.5-pro",
    },

    "claude": {
        "class": ClaudeProvider,
        "topic_file": "claude_topics.txt",
        "output_file": "claude.jsonl",
        "model": "claude-sonnet-4",
    },
}


# ============================================================
# TOPIC SPLITTING
# ============================================================

def divide_topics():

    if not MASTER_TOPIC_FILE.exists():

        raise FileNotFoundError(
            f"Master topic file not found:\n"
            f"{MASTER_TOPIC_FILE}"
        )

    topics = load_topics(
        MASTER_TOPIC_FILE
    )

    if not topics:

        raise ValueError(
            "topics.txt is empty."
        )

    total = len(topics)

    print()
    print("=" * 60)
    print("DIVIDING TOPICS")
    print("=" * 60)

    print(
        f"Total topics: {total}"
    )

    # Divide as evenly as possible.
    base_size = total // 3
    remainder = total % 3

    sizes = [
        base_size + (1 if i < remainder else 0)
        for i in range(3)
    ]

    start = 0

    provider_names = [
        "openai",
        "gemini",
        "claude"
    ]

    for provider_name, size in zip(
        provider_names,
        sizes
    ):

        provider_info = PROVIDERS[
            provider_name
        ]

        end = start + size

        provider_topics = topics[
            start:end
        ]

        output_path = (
            TOPICS_DIR
            / provider_info["topic_file"]
        )

        with output_path.open(
            "w",
            encoding="utf-8"
        ) as file:

            for topic in provider_topics:

                file.write(
                    topic.strip()
                    + "\n"
                )

        print(
            f"{provider_name:<10} "
            f"{len(provider_topics):>4} topics "
            f"-> {output_path.name}"
        )

        start = end

    print("=" * 60)
    print("TOPIC DIVISION COMPLETE")
    print("=" * 60)
    print()


# ============================================================
# LOAD ALREADY GENERATED TOPICS
# ============================================================

def get_completed_topics(
    output_file
):

    output_file = Path(
        output_file
    )

    if not output_file.exists():

        return set()

    completed = set()

    with output_file.open(
        "r",
        encoding="utf-8"
    ) as file:

        for line_number, line in enumerate(
            file,
            start=1
        ):

            line = line.strip()

            if not line:
                continue

            try:

                record = json.loads(
                    line
                )

            except json.JSONDecodeError:

                print(
                    f"Warning: invalid JSON "
                    f"on line {line_number}"
                )

                continue

            topic = record.get(
                "topic"
            )

            if topic:

                completed.add(
                    topic.strip()
                )

    return completed


# ============================================================
# GENERATE ONE ESSAY
# ============================================================

def generate_one(
    provider,
    topic,
    provider_name,
    model_name
):

    max_retries = 3

    for attempt in range(
        1,
        max_retries + 1
    ):

        try:

            essay = provider.generate(
                topic
            )

            if not essay:

                raise ValueError(
                    "Provider returned empty text."
                )

            essay = essay.strip()

            return {
                "essay_id": str(
                    uuid.uuid4()
                ),

                "text": essay,

                "label": "ai",

                "source": provider_name,

                "model": model_name,

                "topic": topic,
            }

        except Exception as exc:

            error = str(exc)

            # ------------------------------------------------
            # QUOTA / CREDIT ERRORS
            # ------------------------------------------------

            quota_errors = [
                "insufficient_quota",
                "credit_balance_exhausted",
                "quota",
                "billing",
            ]

            if any(
                item.lower() in error.lower()
                for item in quota_errors
            ):

                print()
                print(
                    "API QUOTA / CREDIT EXHAUSTED."
                )

                print(
                    "Stopping generation."
                )

                raise RuntimeError(
                    "API quota exhausted."
                ) from exc

            # ------------------------------------------------
            # RATE LIMIT
            # ------------------------------------------------

            if (
                "429" in error
                or "rate limit" in error.lower()
            ):

                if attempt == max_retries:

                    raise RuntimeError(
                        "Rate limit retry limit reached."
                    ) from exc

                wait_time = 2 ** attempt

                print(
                    f"Rate limited. "
                    f"Retrying in "
                    f"{wait_time}s..."
                )

                time.sleep(
                    wait_time
                )

                continue

            # ------------------------------------------------
            # OTHER API ERRORS
            # ------------------------------------------------

            if attempt == max_retries:

                print(
                    f"Generation failed: {error}"
                )

                return None

            wait_time = 2 ** attempt

            print(
                f"Attempt {attempt} failed."
            )

            print(
                f"Retrying in "
                f"{wait_time}s..."
            )

            time.sleep(
                wait_time
            )

    return None


# ============================================================
# GENERATE DATASET
# ============================================================

def generate_dataset(
    provider_name
):

    if provider_name not in PROVIDERS:

        raise ValueError(
            f"Unknown provider: "
            f"{provider_name}"
        )

    info = PROVIDERS[
        provider_name
    ]

    topic_file = (
        TOPICS_DIR
        / info["topic_file"]
    )

    output_file = (
        RAW_AI_DIR
        / info["output_file"]
    )

    # --------------------------------------------------------
    # Verify topic file
    # --------------------------------------------------------

    if not topic_file.exists():

        raise FileNotFoundError(
            f"Topic file not found:\n"
            f"{topic_file}\n\n"
            f"Run the following first:\n"
            f"python -m "
            f"humantrace.generation.generate_dataset "
            f"--divide"
        )

    # --------------------------------------------------------
    # Load topics
    # --------------------------------------------------------

    topics = load_topics(
        topic_file
    )

    # --------------------------------------------------------
    # Existing topics
    # --------------------------------------------------------

    completed = get_completed_topics(
        output_file
    )

    remaining_topics = [
        topic
        for topic in topics
        if topic not in completed
    ]

    # --------------------------------------------------------
    # Create provider
    # --------------------------------------------------------

    provider_class = info[
        "class"
    ]

    provider = provider_class()

    model_name = info[
        "model"
    ]

    # --------------------------------------------------------
    # Display information
    # --------------------------------------------------------

    print()

    print("=" * 60)
    print("HumanTrace AI DATASET GENERATION")
    print("=" * 60)

    print(
        f"Provider          : {provider_name}"
    )

    print(
        f"Model             : {model_name}"
    )

    print(
        f"Topic file        : {topic_file}"
    )

    print(
        f"Output file       : {output_file}"
    )

    print(
        f"Total topics      : {len(topics)}"
    )

    print(
        f"Already generated : {len(completed)}"
    )

    print(
        f"Remaining         : {len(remaining_topics)}"
    )

    print("=" * 60)
    print()

    if not remaining_topics:

        print(
            "All topics have already "
            "been generated."
        )

        return

    # --------------------------------------------------------
    # Generate
    # --------------------------------------------------------

    successful = 0
    failed = 0

    for index, topic in enumerate(
        remaining_topics,
        start=1
    ):

        print(
            f"[{index}/{len(remaining_topics)}] "
            f"{topic}"
        )

        try:

            record = generate_one(
                provider=provider,
                topic=topic,
                provider_name=provider_name,
                model_name=model_name,
            )

        except RuntimeError as exc:

            print()
            print(
                f"STOPPED: {exc}"
            )

            break

        if record is None:

            failed += 1

            print(
                "Failed - skipped.\n"
            )

            continue

        # ----------------------------------------------------
        # Save immediately
        # ----------------------------------------------------

        append_jsonl(
            output_file,
            record
        )

        successful += 1

        print(
            "Saved."
        )

        print()

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    print()
    print("=" * 60)
    print("GENERATION SUMMARY")
    print("=" * 60)

    print(
        f"Provider   : {provider_name}"
    )

    print(
        f"Successful : {successful}"
    )

    print(
        f"Failed     : {failed}"
    )

    print(
        f"Output     : {output_file}"
    )

    print("=" * 60)
    print()


# ============================================================
# COMMAND LINE
# ============================================================

def main():

    parser = argparse.ArgumentParser(
        description=(
            "HumanTrace AI dataset "
            "generation pipeline"
        )
    )

    parser.add_argument(
        "--divide",
        action="store_true",
        help=(
            "Divide topics.txt into "
            "GPT, Gemini and Claude files."
        )
    )

    parser.add_argument(
        "--provider",
        choices=[
            "openai",
            "gemini",
            "claude"
        ],
        help=(
            "Provider to use for generation."
        )
    )

    args = parser.parse_args()

    # --------------------------------------------------------
    # Divide only
    # --------------------------------------------------------

    if args.divide:

        divide_topics()

        return

    # --------------------------------------------------------
    # Generation requires provider
    # --------------------------------------------------------

    if not args.provider:

        parser.error(
            "Use --divide or "
            "--provider <openai|gemini|claude>"
        )

    generate_dataset(
        args.provider
    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()