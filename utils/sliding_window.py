import collections.abc
import typing

T = typing.TypeVar('T')


def sliding_window(
        list_to_split: typing.Sequence[T], window_size: int, step: int
) -> collections.abc.Iterator[typing.List[T]]:
    """Yield sliding n-sized windows from lst."""
    for i in range(0, len(list_to_split), step):
        yield list_to_split[i:i + window_size]
