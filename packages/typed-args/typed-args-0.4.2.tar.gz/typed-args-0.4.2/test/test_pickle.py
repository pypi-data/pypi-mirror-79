from typed_args import TypedArgs, add_argument, dataclass
import pickle
from typing import *


@dataclass()
class Args(TypedArgs):
    foo: Optional[str] = add_argument('--foo')


def test_pickle():
    args = Args.from_args([])

    try:
        _pickled_args = pickle.dumps(args)
    except Exception as e:
        raise e


if __name__ == "__main__":
    test_pickle()
