import typing

T = typing.TypeVar('T')


def chunks(list_to_split: typing.Sized[T], chunk_size: int) -> typing.Generator[typing.List[T]]:
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(list_to_split), chunk_size):
        yield list_to_split[i:i + chunk_size]
