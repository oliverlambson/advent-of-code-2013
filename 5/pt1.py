from tqdm import tqdm
import logging
from typing import Callable
from pathlib import Path
from dataclasses import dataclass


@dataclass
class Targets:
    name: str
    numbers: list[int]


@dataclass
class Map:
    base: str
    target: str
    mapping: Callable[[int], int]


def parse_map(map_raw: str) -> Map:
    m = map_raw.strip().split("\n")
    base, target = map(lambda s: s.strip(), m[0].rstrip(" map:").split("-to-"))
    mappings_raw = map(lambda s: s.strip(), m[1:])

    mapping_fns = []
    for mapping_raw in (mappings_raw):
        range_strings = mapping_raw.split()
        target_start, base_start, length = list(map(int, range_strings))
        base_range = range(base_start, base_start+length)
        target_range = range(target_start, target_start+length)
        # mapping = {base: target for base, target in zip(base_range, target_range)}
        def mapping_fn(x: int) -> int | None:
            logging.debug(f"{base_range}:{target_range} {x}")
            if x not in base_range:
                return None
            idx = x - base_range.start
            return target_range[idx]
        mapping_fns.append(mapping_fn)

    def master_mapping_fn(x: int) -> int:
        logging.debug(mapping_fns)
        for mapping_fn in mapping_fns:
            logging.debug(f"trying {mapping_fn}")
            res = mapping_fn(x)
            if res is not None:
                logging.debug(f"{base} {x} to {target} {res}")
                return res
        # default
        logging.debug(f"no mapping found for {x}")
        res = x
        logging.debug(f"{base} {x} to {target} {res} (default)")
        return res

    return Map(
        base=base,
        target=target,
        mapping=master_mapping_fn,
    )

def derive_map(base: str, target: str, mappings: dict[str, Map]) -> Callable[[int], int]:
    current_map = mappings.get(base)
    if current_map is None:
        raise Exception
    map_fn = current_map.mapping
    if current_map.target == target:
        return map_fn
    return lambda x: derive_map(current_map.target, target, mappings)(map_fn(x))

# def main():
input_file_name = "input.txt"
TEST = True
if TEST:
    logging.basicConfig(level=logging.DEBUG)
    input_file_name = "example_input.txt"
input_file = Path(__file__).parent / input_file_name
input_file_txt = input_file.read_text().strip()

input_blocks = input_file_txt.split("\n\n")

targets_raw = input_blocks[0]
maps_raw = input_blocks[1:]

targets = Targets(
    name=targets_raw.split(": ")[0],
    numbers=list(map(int, targets_raw.split(": ")[1].split()))
)

mappings = {}
for map_raw in maps_raw:
    logging.debug(map_raw)
    m = parse_map(map_raw)
    mappings[m.base] = m
    logging.debug("")

seed_to_location = derive_map("seed", "location", mappings)
locations = map(seed_to_location, targets.numbers)
print(min(locations))



# if __name__ == '__main__':
#     main()
