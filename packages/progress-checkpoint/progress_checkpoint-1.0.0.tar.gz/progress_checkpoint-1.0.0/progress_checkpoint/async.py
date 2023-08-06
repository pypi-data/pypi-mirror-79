from typing import Sequence, Iterable

from .common import AsyncCheckpoint


async def with_progress_async(seq: Iterable, checkpoint: AsyncCheckpoint, size=None, status=None, div=1):
    await checkpoint(0, status or '')
    if size is None:
        if not isinstance(seq, Sequence):
            seq = list(seq)
        size = len(seq)

    for i, e in enumerate(seq):
        yield e

        if i % div == 0:
            await checkpoint(i / size, status)


# noinspection PyUnusedLocal
async def dummy_checkpoint_async(progress, status=None):
    return
