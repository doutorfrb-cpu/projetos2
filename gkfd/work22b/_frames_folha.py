import os, subprocess
BASE = os.path.dirname(os.path.abspath(__file__))
os.environ["PATH"] = BASE + os.pathsep + os.environ.get("PATH", "")
src = os.path.join(BASE, "pc_gkfd24", "gkfd_folha_encargos_reel.mp4")
out = os.path.join(BASE, "_frames_folha")
os.makedirs(out, exist_ok=True)
for t in ("2.0", "7.0", "12.5"):
    subprocess.run(["ffmpeg", "-y", "-ss", t, "-i", src, "-frames:v", "1",
                    os.path.join(out, f"f{t}.png")], capture_output=True)
print(os.listdir(out))
