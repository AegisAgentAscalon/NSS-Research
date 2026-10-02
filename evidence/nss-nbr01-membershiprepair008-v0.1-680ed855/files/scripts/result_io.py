"""Lossless evidence transport. .npz.xz decompresses to identical original bytes.

This is archival compression, not low-bit neural state or an inference mechanism.
"""
from pathlib import Path
import io,lzma,hashlib
import numpy as np

def result_bytes(path):
    p=Path(path)
    if p.exists():return p.read_bytes()
    compressed=Path(str(p)+'.xz')
    if compressed.exists():return lzma.decompress(compressed.read_bytes())
    raise FileNotFoundError(p)

def open_result(path):return np.load(io.BytesIO(result_bytes(path)),allow_pickle=False)
def result_sha(path):return hashlib.sha256(result_bytes(path)).hexdigest()
