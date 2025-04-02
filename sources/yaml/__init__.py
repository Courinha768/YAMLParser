from io import TextIOWrapper
from typing import Any
from yaml.decoder import YAMLDecodeError, YAMLDecoder

_default_decoder = YAMLDecoder()

def load(fp : TextIOWrapper) -> Any:
	"""
	Deserialize ``fp`` (a ``.read()``-supporting file-like object containing a YAML document) to a Python object.
	"""
	return loads(fp.read())

def loads(s : str) -> Any:
	"""
	Deserialize ``s`` (a ``str``, ``bytes`` or ``bytearray`` instance containing a JSON document) to a Python object.
	"""
	if isinstance(s, str):
		if s.startswith('\ufeff'):
			raise YAMLDecodeError("Unexpected UTF-8 BOM (decode using utf-8-sig)",					  s, 0)
	else:
		if not isinstance(s, (bytes, bytearray)):
			raise TypeError(f'the JSON object must be str, bytes or bytearray, '
							f'not {s.__class__.__name__}')

	return _default_decoder.decode(s)
