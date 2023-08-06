from typing import Sequence, Iterable, Union, Sized

from deprecation import deprecated

from .common import Checkpoint, subcheckpoint, subcheckpoints


# noinspection PyUnusedLocal
def dummy_checkpoint(progress, status=None):
    return


def with_progress(seq: Iterable, checkpoint: Checkpoint, size=None, status=None, div=1):
    checkpoint(0, status or '')
    if size is None:
        assert isinstance(seq, Sized), '`seq` must be a sequence unless `size` is given'
        size = len(seq)

    for i, e in enumerate(seq):
        yield e

        if i % div == 0:
            checkpoint(i / size, status)

    checkpoint(1.0, status)


def with_progress_sub(seq: Iterable, checkpoint: Checkpoint, size=None, status=None, statuses=None, status_pattern=None,
                      weights: Iterable[float] = None, div=1):
    if size is None:
        assert isinstance(seq, Sized), '`seq` must be a sequence unless `size` is given'
        size = len(seq)

    checkpoints = subcheckpoints(checkpoint, weights=weights, statuses=statuses, status_pattern=status_pattern,
                                 size=size)

    if isinstance(seq, Sequence):
        assert (len(seq) == size)

    checkpoint(0, status or '')

    for i, (e, c) in enumerate(zip(seq, checkpoints)):
        yield e, c

        if i % div == 0:
            c(1.0)