import sys
import builtins
from pathlib import Path

# Ensure src module is in the path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.main import main  # noqa: E402

# Simulated inputs
inputs = [
    "1", # Select 'Book Management'
    "2", # Select 'List Books' to see seeded data
    "6", # Back to main menu
    "2", # Select 'Member Management'
    "1", # Select 'Register Member'
    "Tony Stark", # Enter Name
    "ironman@avengers.com", # Enter Email
    "2", # Select 'List Members' to verify
    "6", # Back to main menu
    "4"  # Exit
]

original_input = builtins.input

def mock_input(prompt=""):
    if not inputs:
        print(prompt + " [EOF]")
        raise EOFError()
    val = inputs.pop(0)
    # Print the prompt and the simulated user input so the output looks like a real terminal
    print(f"{prompt}{val}")
    return val

builtins.input = mock_input

if __name__ == "__main__":
    print("=== STARTING CLI SIMULATION ===\n")
    try:
        main()
    except Exception as e:
        print(f"\nSimulation ended with exception: {e}")
    finally:
        builtins.input = original_input
    print("\n=== END OF SIMULATION ===")
