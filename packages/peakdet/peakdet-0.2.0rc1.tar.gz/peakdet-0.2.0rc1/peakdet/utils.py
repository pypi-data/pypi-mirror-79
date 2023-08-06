# -*- coding: utf-8 -*-
"""
Various utilities for processing physiological data. These should not be called
directly but should support wrapper functions stored in `peakdet.operations`.
"""

from functools import wraps
import inspect
import numpy as np
from peakdet import physio


def make_operation(*, exclude=None):
    """
    Wrapper to make functions into Physio operations

    Wrapped functions should accept a :class:`peakdet.Physio` instance, `data`,
    as their first parameter, and should return a :class:`peakdet.Physio`
    instance

    Parameters
    ----------
    exclude : list, optional
        What function parameters to exclude from being stored in history.
        Default: 'data'
    """

    def get_call(func):
        @wraps(func)
        def wrapper(data, *args, **kwargs):
            # exclude 'data', by default
            ignore = ['data'] if exclude is None else exclude

            # grab parameters from `func` by binding signature
            name = func.__name__
            sig = inspect.signature(func)
            params = sig.bind(data, *args, **kwargs).arguments

            # actually run function on data
            data = func(data, *args, **kwargs)

            # it shouldn't be, but don't bother appending to history if it is
            if data is None:
                return data

            # get parameters and sort by key name, dropping ignored items and
            # attempting to coerce any numpy arrays or pandas dataframes (?!)
            # into serializable objects; this isn't foolproof but gets 80% of
            # the way there
            provided = {k: params[k] for k in sorted(params.keys())
                        if k not in ignore}
            for k, v in provided.items():
                if hasattr(v, 'tolist'):
                    provided[k] = v.tolist()

            # append everything to data instance history
            data._history += [(name, provided)]

            return data
        return wrapper
    return get_call


def _get_call(*, exclude=None, serializable=True):
    """
    Returns calling function name and dict of provided arguments (name : value)

    Parameters
    ----------
    exclude : list, optional
        What arguments to exclude from provided argument : value dictionary.
        Default: ['data']
    serializable : bool, optional
        Whether to coerce argument values to JSON serializable form. Default:
        True

    Returns
    -------
    function: str
        Name of calling function
    provided : dict
        Dictionary of function arguments and provided values
    """

    exclude = ['data'] if exclude is None else exclude
    if not isinstance(exclude, list):
        exclude = [exclude]

    # get one function call up the stack (the bottom is _this_ function)
    calling = inspect.stack(0)[1]
    frame, function = calling.frame, calling.function

    # get all the args / kwargs from the calling function
    argspec = inspect.getfullargspec(frame.f_globals[function])
    args = sorted(argspec.args + argspec.kwonlyargs)

    # save arguments + argument values for everything not in `exclude`
    provided = {k: frame.f_locals[k] for k in args if k not in exclude}

    # if we want `provided` to be serializable, we can do a little cleaning up
    # this is NOT foolproof, but will coerce numpy arrays to lists which tends
    # to be the main issue with these sorts of things
    if serializable:
        for k, v in provided.items():
            if hasattr(v, 'tolist'):
                provided[k] = v.tolist()

    return function, provided


def check_physio(data, ensure_fs=True, copy=False):
    """
    Checks that `data` is in correct format (i.e., `peakdet.Physio`)

    Parameters
    ----------
    data : Physio_like
    ensure_fs : bool, optional
        Raise ValueError if `data` does not have a valid sampling rate
        attribute.
    copy: bool, optional
        Whether to return a copy of the provided data. Default: False

    Returns
    -------
    data : peakdet.Physio
        Loaded physio object

    Raises
    ------
    ValueError
        If `ensure_fs` is set and `data` doesn't have valid sampling rate
    """

    from peakdet.io import load_physio

    if not isinstance(data, physio.Physio):
        data = load_physio(data)
    if ensure_fs and np.isnan(data.fs):
        raise ValueError('Provided data does not have valid sampling rate.')
    if copy is True:
        return new_physio_like(data, data.data,
                               copy_history=True,
                               copy_metadata=True)
    return data


def new_physio_like(ref_physio, data, *, fs=None, dtype=None,
                    copy_history=True, copy_metadata=True):
    """
    Makes `data` into physio object like `ref_data`

    Parameters
    ----------
    ref_physio : Physio_like
        Reference `Physio` object
    data : array_like
        Input physiological data
    fs : float, optional
        Sampling rate of `data`. If not supplied, assumed to be the same as
        in `ref_physio`
    dtype : data_type, optional
        Data type to convert `data` to, if conversion needed. Default: None
    copy_history : bool, optional
        Copy history from `ref_physio` to new physio object. Default: True

    Returns
    -------
    data : peakdet.Physio
        Loaded physio object with provided `data`
    """

    if fs is None:
        fs = ref_physio.fs
    if dtype is None:
        dtype = ref_physio.data.dtype
    history = list(ref_physio.history) if copy_history else []
    metadata = dict(**ref_physio._metadata) if copy_metadata else None

    # make new class
    out = ref_physio.__class__(np.array(data, dtype=dtype),
                               fs=fs, history=history, metadata=metadata)
    return out


def check_troughs(data, peaks):
    """
    Confirms that `troughs` exists between every set of `peaks` in `data`

    Parameters
    ----------
    data : array-like
        Input data for which `troughs` and `peaks` were detected
    peaks : array-like
        Indices of suspected peak locations in `data`

    Returns
    -------
    troughs : np.ndarray
        Indices of trough locations in `data`, dependent on `peaks`
    """

    all_troughs = np.zeros(peaks.size - 1, dtype=int)

    for f in range(peaks.size - 1):
        dp = data[peaks[f]:peaks[f + 1]]
        idx = peaks[f] + np.argwhere(dp == dp.min())[0]
        all_troughs[f] = idx

    return all_troughs
