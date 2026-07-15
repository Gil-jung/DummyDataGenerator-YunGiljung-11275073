import argparse
import sys

from dummygen.generator import generate_records
from dummygen.schema import SchemaError, load_schema
from dummygen.writer import write_json


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="dummy-gen")
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate = subparsers.add_parser("generate", help="Generate dummy data from a schema")
    generate.add_argument("--schema", required=True, help="Path to the schema JSON file")
    generate.add_argument("--count", type=int, default=1, help="Number of records to generate")
    generate.add_argument("--output", required=True, help="Path to write the generated JSON file")
    generate.add_argument("--seed", type=int, default=None, help="Random seed for reproducible output")

    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "generate":
        try:
            schema = load_schema(args.schema)
        except SchemaError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1

        records = generate_records(schema, count=args.count, seed=args.seed)
        write_json(records, args.output)
        return 0

    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    sys.exit(main())
