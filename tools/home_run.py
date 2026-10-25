# The nightly job on the owner's Windows computer, started by tools/windows/run.bat (Task Scheduler, 23:00).
# A home connection is not blocked by YouTube the way GitHub's servers are, so the collecting happens here:
#  1. sync with the latest main, 2. collect new clips into home-clips/ for up to 7 hours,
#  3. sync again, merge the clips into the published corpus, recount lessons, commit and push.
# Clips stay in home-clips/ until a push succeeds, so nothing is lost if the computer is switched off.
# The end of the collector's output is published as tools/home-log.txt every night, even when nothing was collected,
# so a Claude session can see what happened without asking the owner for screenshots.
# Usage: python -X utf8 -I tools/home_run.py <git.exe> <node.exe>
import collections, ctypes, glob, os, shutil, subprocess, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLIPS = os.path.join(ROOT, 'home-clips')
LOG = os.path.join(ROOT, 'tools', 'home-log.txt')
tail = collections.deque(maxlen=400)
GIT, NODE = sys.argv[1], sys.argv[2]
PY = [sys.executable, '-X', 'utf8', '-I', os.path.join(ROOT, 'tools', 'update_corpus.py')]

def run(cmd, check=True):
    print('>', ' '.join(cmd), flush=True)
    return subprocess.run(cmd, cwd=ROOT, check=check)

def sync():
    run([GIT, 'fetch', 'origin', 'main'])
    run([GIT, 'reset', '--hard', 'FETCH_HEAD'])

def collect(cmd):
    """Run the collector, passing its output through to collect.log and keeping the end of it for home-log.txt."""
    print('>', ' '.join(cmd), flush=True)
    p = subprocess.Popen(cmd, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')
    for line in p.stdout:
        print(line, end='', flush=True); tail.append(time.strftime('%H:%M:%S ') + line.rstrip('\n'))
    p.wait()

def build(clips):
    with open(LOG, 'w', encoding='utf-8') as o:
        o.write('Nightly run on the home computer, ' + time.strftime('%Y-%m-%d %H:%M') + ' (last 400 lines of the collector)\n')
        o.write('\n'.join(tail) + '\n')
    if os.path.isdir(CLIPS):  # also when only skip.json is there, so rejected clips are remembered
        run(PY + ['--merge-dir', CLIPS])
        run([NODE, os.path.join('tools', 'count_lessons.js')])
    run([GIT, 'add', '-A', '--', 'data.js', 'data-*.js', 'counts.js', 'tools/corpus-skip.json', 'tools/home-log.txt'])
    if subprocess.run([GIT, 'diff', '--cached', '--quiet'], cwd=ROOT).returncode == 0: return False
    run([GIT, 'commit', '-m', 'Add clips collected on the home computer' if clips else 'Home computer: run log (no new clips)'])
    return True

def main():
    print('==== start', time.strftime('%Y-%m-%d %H:%M'), '====', flush=True)
    if os.name == 'nt':  # keep the computer awake while this runs (ES_CONTINUOUS | ES_SYSTEM_REQUIRED)
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | 0x00000001)
    sync()
    collect(PY + ['--save-dir', CLIPS, '--limit', '1500', '--minutes', '420', '--per-channel', '40', '--depth', '500',
                  '--wait-when-blocked', '20'])
    clips = [f for f in glob.glob(os.path.join(CLIPS, '*.json')) if os.path.basename(f) != 'skip.json']
    if not clips: print('nothing collected; publishing the log only', flush=True)
    for attempt in range(3):
        sync()
        if not build(clips): print('no changes to publish'); break
        if run([GIT, 'push', 'origin', 'HEAD:main'], check=False).returncode == 0:
            print('published', flush=True); break
        time.sleep(60)  # someone else pushed meanwhile: rebuild on top of theirs
    else:
        print('could not push; the clips stay in home-clips/ for the next night'); return
    shutil.rmtree(CLIPS, ignore_errors=True)
    print('==== done', time.strftime('%Y-%m-%d %H:%M'), '====', flush=True)

if __name__ == '__main__':
    main()
