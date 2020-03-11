import numpy as np
from tianshou.data.batch import Batch


class ReplayBuffer(object):
    """docstring for ReplayBuffer"""
    def __init__(self, size):
        super().__init__()
        self._maxsize = size
        self._index = self._size = 0

    def __len__(self):
        return self._size

    def _add_to_buffer(self, name, inst):
        if inst is None:
            return
        if self.__dict__.get(name, None) is None:
            if isinstance(inst, np.ndarray):
                self.__dict__[name] = np.zeros([self._maxsize, *inst.shape])
            elif isinstance(inst, dict):
                self.__dict__[name] = np.array([{} for _ in range(self._maxsize)])
            else: # assume `inst` is a number
                self.__dict__[name] = np.zeros([self._maxsize])
        self.__dict__[name][self._index] = inst

    def add(self, obs, act, rew, done, obs_next=0, info={}, weight=None):
        '''
        weight: importance weights, disabled here
        '''
        assert isinstance(info, dict), 'You should return a dict in the last argument of env.step function.'
        self._add_to_buffer('obs', obs)
        self._add_to_buffer('act', act)
        self._add_to_buffer('rew', rew)
        self._add_to_buffer('done', done)
        self._add_to_buffer('obs_next', obs_next)
        self._add_to_buffer('info', info)
        self._size = min(self._size + 1, self._maxsize)
        self._index = (self._index + 1) % self._maxsize

    def reset(self):
        self._index = self._size = 0

    def sample_indice(self, batch_size):
        return np.random.choice(self._size, batch_size)

    def sample(self, batch_size):
        indice = self.sample_index(batch_size)
        return Batch(obs=self.obs[indice], act=self.act[indice], rew=self.rew[indice], 
            done=self.done[indice], obs_next=self.obs_next[indice], info=self.info[indice])


class PrioritizedReplayBuffer(ReplayBuffer):
    """docstring for PrioritizedReplayBuffer"""
    def __init__(self, size):
        super().__init__(size)
    
    def add(self, obs, act, rew, done, obs_next, info={}, weight=None):
        raise NotImplementedError

    def sample_indice(self, batch_size):
        raise NotImplementedError

    def sample(self, batch_size):
        raise NotImplementedError