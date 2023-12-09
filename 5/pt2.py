import logging
from typing import Callable, Iterator
from pathlib import Path
from dataclasses import dataclass

from tqdm import tqdm


@dataclass
class Targets:
    name: str
    numbers: Iterator[int]
    length: int | None = None


@dataclass
class Map:
    base: str
    target: str
    mapping: Callable[[int], int]


def mapping_fn_factory(base_range, target_range) -> Callable[[int], int | None]:
    def inner(x: int) -> int | None:
        # logging.debug(f"{base_range}:{target_range} {x}")
        if x not in base_range:
            return None
        idx = x - base_range.start
        return target_range[idx]

    return inner


def parse_map(map_raw: str) -> Map:
    m = map_raw.strip().split("\n")
    base, target = map(lambda s: s.strip(), m[0].rstrip(" map:").split("-to-"))
    mappings_raw = map(lambda s: s.strip(), m[1:])

    mapping_fns: list[Callable[[int], int | None]] = []
    for mapping_raw in mappings_raw:
        range_strings = mapping_raw.split()
        target_start, base_start, length = list(map(int, range_strings))
        base_range = range(base_start, base_start + length)
        target_range = range(target_start, target_start + length)
        mapping_fn = mapping_fn_factory(base_range, target_range)
        mapping_fns.append(mapping_fn)

    def master_mapping_fn(x: int) -> int:
        # logging.debug(mapping_fns)
        for mapping_fn in mapping_fns:
            # logging.debug(f"trying {mapping_fn}")
            res = mapping_fn(x)
            if res is not None:
                # logging.debug(f"{base} {x} to {target} {res}")
                return res
        # default
        # logging.debug(f"no mapping found for {x}")
        res = x
        # logging.debug(f"{base} {x} to {target} {res} (default)")
        return res

    return Map(
        base=base,
        target=target,
        mapping=master_mapping_fn,
    )


def derive_map(
    base: str, target: str, mappings: dict[str, Map]
) -> Callable[[int], int]:
    current_map = mappings.get(base)
    if current_map is None:
        raise Exception
    map_fn = current_map.mapping
    if current_map.target == target:
        return map_fn
    return lambda x: derive_map(current_map.target, target, mappings)(map_fn(x))


def get_target_numbers(raw: str) -> Iterator[int]:
    input_numbers = list(map(int, raw.split()))
    n_tuples = [
        (input_numbers[i], input_numbers[i + 1])
        for i in range(0, len(input_numbers), 2)
    ]
    ranges = [range(start, start + n) for start, n in n_tuples]
    for r in ranges:
        for x in r:
            yield x


def get_target_numbers_len(raw: str) -> int:
    input_numbers = list(map(int, raw.split()))
    n_tuples = [
        (input_numbers[i], input_numbers[i + 1])
        for i in range(0, len(input_numbers), 2)
    ]
    ranges = [range(start, start + n) for start, n in n_tuples]
    length = sum(map(len, ranges))
    return length


def main():
    input_file_name = "input.txt"
    loglevel = logging.INFO
    TEST = False
    if TEST:
        loglevel = logging.DEBUG
        input_file_name = "example_input.txt"
    input_file = Path(__file__).parent / input_file_name
    logging.basicConfig(level=loglevel)
    input_file_txt = input_file.read_text().strip()

    input_blocks = input_file_txt.split("\n\n")

    targets_raw = input_blocks[0]
    maps_raw = input_blocks[1:]

    logging.info("Getting targets")
    targets = Targets(
        name=targets_raw.split(": ")[0],
        numbers=get_target_numbers(targets_raw.split(": ")[1]),
        length=get_target_numbers_len(targets_raw.split(": ")[1]),
    )

    mappings = {}
    logging.info("Parsing maps")
    for map_raw in maps_raw:
        logging.debug(map_raw)
        m = parse_map(map_raw)
        mappings[m.base] = m
        logging.debug("")

    seed_to_location = derive_map("seed", "location", mappings)

    logging.info("Mapping seed to location")
    locations = map(seed_to_location, tqdm(targets.numbers, total=targets.length))
    logging.info("Finding min location")
    min_location = min(locations)
    if TEST:
        assert min_location == 46
        print("✅ pass")
    print(f"{min_location=}")


if __name__ == "__main__":
    main()
