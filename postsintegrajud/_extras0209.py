import os, shutil, glob

dst = '2026-09-02_conversao-sacas-laudo'
story = glob.glob('work0209/kit_anuncios/*916*.png')
reel = glob.glob('work0209/pc_0209_conversao_sacas/*reel*.mp4')
print('story origem:', story)
print('reel origem:', reel)
shutil.copy(story[0], os.path.join(dst, 'story_916.png'))
shutil.copy(reel[0], os.path.join(dst, 'reel.mp4'))
print(sorted(os.listdir(dst)))
