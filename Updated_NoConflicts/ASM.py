import os, tempfile, subprocess
from ctypes import CDLL

def build_and_load_asm(asm_text, mode="auto"):
    """
    Builds and runs inline ASM by generating a C wrapper,
    compiling it into a shared object, loading it via ctypes,
    and executing the function.

    Parameters:
        asm_text (str): Raw assembly code (GCC inline asm syntax)
        mode (str): 'auto', 'native', or 'simulate'
    """
    # === 1. Generate temporary folder and file ===
    workdir = tempfile.mkdtemp(prefix="diamant_asm_")
    c_path = os.path.join(workdir, "inline_asm.c")
    so_path = os.path.join(workdir, "libinline_asm.so")

    # === 2. Build the C wrapper code ===
    c_code = f'''
    #include <stdint.h>
    void inline_asm_fn(void) {{
        asm({asm_text});
    }}
    '''
    print(c_code)

    with open(c_path, "w") as f:
        f.write(c_code)

    # === 3. Compile with gcc ===
    gcc_cmd = ["gcc", "-shared", "-fPIC","-m64" ,c_path, "-o", so_path]
    proc = subprocess.run(gcc_cmd, capture_output=True, text=True)

    if proc.returncode != 0:
        print("[!] GCC compilation failed.")
        print(proc.stderr)
        return None

    # === 4. Load compiled library ===
    lib = CDLL(so_path)

    # === 5. Execute the function ===
    try:
        func = lib.inline_asm_fn
        func.restype = None
        func()
        print("[+] ASM executed successfully!")
    except Exception as e:
        print("[!] Error executing ASM:", e)

    print(f"[info] Temp files stored in: {workdir}")
    return lib
