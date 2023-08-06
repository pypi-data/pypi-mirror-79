from itertools import cycle

"""An RL Sampling Running built with (pyTorch) Multiprocessing"""

USE_TORCH_MP = True


class DummyRunner:
    _msg = None
    gen_fns = []

    def msg(self, msg):
        self._msg = msg

    def __init__(self, gen_fns, *args, context_fn=None, **kwargs):
        """
        :param worker:
        :param context_fn: a function you can use to create shared memory objects
        """
        kw = context_fn(None) if callable(context_fn) else {}
        kw.update(kwargs)
        self.gen_fns = [f(*args, **kw) for f in gen_fns]

    def __repr__(self):
        return f"<DummyRunner>"

    def trajs(self, msg=None):
        """ yields full trajectories"""
        # if limit is not None:
        #     self._msg = limit
        for gen in cycle(self.gen_fns):
            yield next(gen) if msg is None else gen.send(msg)

    def close(self):
        for gen in self.gen_fns:
            gen.close()

    def __del__(self):
        self.close()


