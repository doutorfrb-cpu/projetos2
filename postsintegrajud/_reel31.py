import os, sys, runpy

BASE = os.path.dirname(os.path.abspath(__file__))
os.environ["PATH"] = BASE + os.pathsep + os.environ.get("PATH", "")
work = os.path.join(BASE, "work31")
sys.path.insert(0, work)
os.chdir(work)
sys.argv = ["reel.py", os.path.join(BASE, "spec_31ago_demonstrativo_524.json")]
runpy.run_path(os.path.join(work, "reel.py"), run_name="__main__")
