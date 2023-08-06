import toml
from pathlib import Path

configPath = Path(__file__).parent.joinpath('config.toml')
config = toml.load(configPath)

def main():
    from .ui import ConsoleUI

if __name__ == '__main__':
    main()
