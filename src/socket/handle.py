
# Useful to handle killing tensorflow process
from src.helpers import kill_all_child
import atexit
atexit.register(kill_all_child)