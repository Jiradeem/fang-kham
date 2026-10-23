# The nightly job on the owner's Windows computer, started by tools/windows/run.bat (Task Scheduler, 23:00).
# A home connection is not blocked by YouTube the way GitHub's servers are, so the collecting happens here:
#  1. sync with the latest main, 2. collect new clips into home-clips/ for up to 7 hours,
#  3. sync again, merge the clips into the published corpus, recount lessons, commit and push.
# Clips stay in home-clips/ until a push succeeds, so nothing is lost if the computer is switched off.
# Usage: python -X utf8 -I tools/home_run.py <git.exe> <node.exe>
import ctypes, glob, os, shutil, subprocess, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLIPS = os.path.join(ROOT, 'home-clips')
GIT, NODE = sys.argv[1], sys.argv[2]
PY = [sys.executable, '-X', 'utf8', '-I', os.path.join(ROOT, 'tools', 'update_corpus.py')]

def run(cmd, check=True):
    print('>', ' '.join(cmd), flush=True)
    return subprocess.run(cmd, cwd=ROOT, check=check)

def sync():
    run([GIT, 'fetch', 'origin', 'main'])
    run([GIT, 'reset', '--hard', 'FETCH_HEAD'])

def build():
    run(PY + ['--merge-dir', CLIPS])
    run([NODE, os.path.join('tools', 'count_lessons.js')])
    run([GIT, 'add', '-A', '--', 'data.js', 'data-*.js', 'counts.js', 'tools/corpus-skip.json'])
    if subprocess.run([GIT, 'diff', '--cached', '--quiet'], cwd=ROOT).returncode == 0: return False
    run([GIT, 'commit', '-m', 'Add clips collected on the home computer'])
    return True

def main():
    print('==== start', time.strftime('%Y-%m-%d %H:%M'), '====', flush=True)
    if os.name == 'nt':  # keep the computer awake while this runs (ES_CONTINUOUS | ES_SYSTEM_REQUIRED)
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | 0x00000001)
    sync()
    run(PY + ['--save-dir', CLIPS, '--limit', '600', '--minutes', '420', '--per-channel', '15', '--depth', '120',
              '--wait-when-blocked', '20'], check=False)
    if not glob.glob(os.path.join(CLIPS, '*.json')): print('nothing collected'); return
    for attempt in range(3):
        sync()
        if not build(): print('no changes to publish'); break
        if run([GIT, 'push', 'origin', 'HEAD:main'], check=False).returncode == 0:
            print('published', flush=True); break
        time.sleep(60)  # someone else pushed meanwhile: rebuild on top of theirs
    else:
        print('could not push; the clips stay in home-clips/ for the next night'); return
    shutil.rmtree(CLIPS, ignore_errors=True)
    print('==== done', time.strftime('%Y-%m-%d %H:%M'), '====', flush=True)

if __name__ == '__main__':
    main()
