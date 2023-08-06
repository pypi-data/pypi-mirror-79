from collections.abc import MutableMapping
import importlib.util
import functools
import inspect
import time


def add_method(cls):
	"""
	Add method to cls
	:param cls: Class
	:return:
	"""
	def decorator(func):
		@functools.wraps(func)
		def wrapper(self, *args, **kwargs):
			return func(*args, **kwargs)
		setattr(cls, func.__name__, wrapper)
		# Note we are not binding func, but wrapper which accepts self but does exactly the same as func
		return func # returning func means func can still be used normally
	return decorator


def get_class_that_defined_method(meth):
	"""
	Get defining class of method
	source: https://stackoverflow.com/a/25959545
	:param meth:
	:return: Example: <class '__main__.RsmJob'>
	"""
	if inspect.ismethod(meth):
		for cls in inspect.getmro(meth.__self__.__class__):
			if meth.__name__ in cls.__dict__:
				return cls
		meth = meth.__func__  # fallback to __qualname__ parsing
	if inspect.isfunction(meth):
		cls = getattr(
			inspect.getmodule(meth),
			meth.__qualname__.split(
				'.<locals>',
				1)[0].rsplit(
				'.',
				1)[0],
			None)
		if isinstance(cls, type):
			return cls
	return None


def get_module_location(mod):
	"""
	List of strings for where to find submodules, if a package (None otherwise).
	:param mod: Module to find the specs.
	:return: submodule_search_locations
	"""
	spec = importlib.util.find_spec(mod)
	return spec.submodule_search_locations


def benchmark(func):
	"""Print the runtime of the decorated function"""

	@functools.wraps(func)
	def wrapper_timer(*args, **kwargs):
		start_time = time.perf_counter()
		value = func(*args, **kwargs)
		end_time = time.perf_counter()
		run_time = end_time - start_time
		print(f"Finished {func.__name__!r} in {run_time:.4f} secs")
		return value

	return wrapper_timer  # no "()" here, we need the object to be returned.


def dict_to_flat(
		dictionary: dict or MutableMapping,
		parent_key: bool = False,
		separator: str = '.') -> dict:
	"""
	Turn a nested dictionary into a flattened dictionary
	:param dictionary: The dictionary to flatten
	:param parent_key: The string to prepend to dictionary's keys
	:param separator: The string used to separate flattened keys
	:return: A flattened dictionary
	"""

	items = []
	for key, value in dictionary.items():
		new_key = str(parent_key) + separator + key if parent_key else key
		if isinstance(value, MutableMapping):
			items.extend(dict_to_flat(value, new_key, separator).items())
		elif isinstance(value, list):
			for k, v in enumerate(value):
				items.extend(dict_to_flat({str(k): v}, new_key).items())
		else:
			items.append((new_key, value))
	return dict(items)