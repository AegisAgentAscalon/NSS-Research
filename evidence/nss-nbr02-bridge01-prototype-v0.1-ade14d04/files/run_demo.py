"""Run one offline dummy episode; output must be a new directory."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent/'source'))
from nss_bridge.runner import main
if __name__=='__main__':
    sys.argv.append('--demo')
    main()
