import os
import tempfile
import subprocess
from ctypes import CDLL

def build_and_load_c_block(c_code, mode="auto", entry_function=None):
    """
    Builds and runs a C block by generating a temporary C file,
    compiling it into a shared library, loading it via ctypes,
    and optionally executing a function.

    Parameters:
        c_code (str): Full C code to compile.
        mode (str): 'auto', '32', or '64' bit compilation mode.
        entry_function (str or None): Name of a function to call after loading.
    """
    # === 1. Generate temporary folder and file ===
    workdir = tempfile.mkdtemp(prefix="diamant_c_")
    c_path = os.path.join(workdir, "temp.c")
    so_path = os.path.join(workdir, "libtemp.so")

    # === 2. Write the C code to file ===
    with open(c_path, "w") as f:
        f.write(c_code)

    # === 3. Compile with GCC ===
    gcc_cmd = ["gcc", "-shared", "-fPIC", c_path, "-o", so_path]
    if mode == "32":
        gcc_cmd.insert(1, "-m32")
    elif mode == "64" or (mode == "auto" and os.name != "nt"):
        gcc_cmd.insert(1, "-m64")

    proc = subprocess.run(gcc_cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        print("[!] GCC compilation failed.")
        print(proc.stderr)
        print(f"[info] command: {' '.join(gcc_cmd)}")
        print(f"[info] temp folder: {workdir}")
        return None

    # === 4. Load compiled library ===
    lib = CDLL(so_path)

    # === 5. Execute the entry function if provided ===
    if entry_function:
        try:
            func = getattr(lib, entry_function)
            func.restype = None
            func()
            print(f"[+] Function '{entry_function}' executed successfully!")
        except Exception as e:
            print(f"[!] Error executing function '{entry_function}':", e)

    print(f"[info] Temp files stored in: {workdir}")
    return lib
