import json
import typing
import random
import logging, sys
import threading
import ctypes
import multiprocessing
import uuid
import time
import inspect

def split_list(lis, ratios, shuffle=False):
    if not lis:
        return None
    if len(lis) < len(ratios):
        raise Exception("List is not long enough to be split.")
    import numpy as np
    if shuffle:
        random.shuffle(lis)
    ratios = np.array(ratios)
    ratios = ratios / ratios.sum()
    nums = ratios * len(lis)
    nums = np.round(nums).astype(int)
    total = len(lis)
    splits = []
    current_index = 0
    for i, num in enumerate(nums):
        end_point = min(current_index + num, total)
        batch = lis[current_index:end_point]
        splits.append(batch)
        current_index = end_point
    return splits

def _async_raise(tid, exctype):
    '''Raises an exception in the threads with id tid'''
    if not inspect.isclass(exctype):
        raise TypeError("Only types can be raised (not instances)")
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid),
                                                     ctypes.py_object(exctype))
    print('res:',res)
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # "if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"
        ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), None)
        raise SystemError("PyThreadState_SetAsyncExc failed")

class KillableThread(threading.Thread):
    '''A thread class that supports raising exception in the thread from
       another thread.
    '''
    _threads={}
    @classmethod
    def start_new_thread(cls,target,name):
        if cls._threads.get(name,None) is not None:
            print('thread %s is running, if you want to rerun it, you need to kill it first.'%(name))
            return
        thread=cls(target=target)
        cls._threads[name]=thread
        thread.start()
    @classmethod
    def kill_thread_by_name(cls,name):
        if name not in cls._threads.keys():
            print('Thread %s not running.'%(name))
            return
        cls._threads[name].kill()
        del cls._threads[name]

    def _get_my_tid(self):
        """determines this (self's) thread id

        CAREFUL : this function is executed in the context of the caller
        thread, to get the identity of the thread represented by this
        instance.
        """
        if not self.isAlive():
            raise threading.ThreadError("the thread is not active")

        # do we have it cached?
        if hasattr(self, "_thread_id"):
            return self._thread_id

        # no, look for it in the _active dict
        for tid, tobj in threading._active.items():
            if tobj is self:
                self._thread_id = tid
                return tid

        # TODO: in python 2.6, there's a simpler way to do : self.ident

        raise AssertionError("could not determine the thread's id")

    def kill(self, exctype=Exception):
        try:
           tid=self._get_my_tid()
           print('killing thread %s'%(tid))
           _async_raise(self._get_my_tid(), exctype)
           self.join()
        except:
            print('Thread has been killed.')




        # self.join()