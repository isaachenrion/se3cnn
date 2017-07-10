'''
Cache in file
'''
from functools import wraps
import pickle
import gzip
import os


def cached_pklgz(filename):
    '''
    Cache a function with a file
    '''
    def decorator(func):
        '''
        The actual decorator
        '''
        @wraps(func)
        def wrapper(*args):
            '''
            The wrapper of the function
            '''
            try:
                with gzip.open(filename, "rb") as file:
                    cache = pickle.load(file)
            except FileNotFoundError:
                cache = {}

            try:
                return cache[args]
            except KeyError:
                cache[args] = result = func(*args)
                with gzip.open(filename, "wb") as file:
                    pickle.dump(cache, file)
                return result
        return wrapper
    return decorator


def cached_dirpklgz(dirname):
    '''
    Cache a function with a directory
    '''
    def decorator(func):
        '''
        The actual decorator
        '''
        @wraps(func)
        def wrapper(*args):
            '''
            The wrapper of the function
            '''
            try:
                os.mkdir(dirname)
            except FileExistsError:
                pass

            indexfile = os.path.join(dirname, "index.pkl")

            try:
                with open(indexfile, "rb") as file:
                    index = pickle.load(file)
            except FileNotFoundError:
                index = {}

            try:
                filename = index[args]
            except KeyError:
                index[args] = filename = os.path.join(dirname, "{}.pkl.gz".format(len(index)))
                with open(indexfile, "wb") as file:
                    pickle.dump(index, file)

            try:
                with gzip.open(filename, "rb") as file:
                    return pickle.load(file)
            except FileNotFoundError:
                print("compute {}".format(filename))
                result = func(*args)
                with gzip.open(filename, "wb") as file:
                    pickle.dump(result, file)
                return result
        return wrapper
    return decorator