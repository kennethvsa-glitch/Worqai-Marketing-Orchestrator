import subprocess
import sys

# Start the render as a detached Windows process
p = subprocess.Popen(
    ['py', 'scripts/motion_exporter.py',
     '--input', 'templates/scenes/scene-launch-villain-v3-quantum.html',
     '--output', 'export-video',
     '--aspect', '9:16',
     '--name', 'villain-v3-quantum-v2'],
    cwd='C:/Users/kenne/motion-studio',
    stdout=open('C:/Users/kenne/motion-studio/render_v2.log', 'w'),
    stderr=subprocess.STDOUT,
    creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
)

with open('C:/Users/kenne/motion-studio/render_v2.pid', 'w') as f:
    f.write(str(p.pid))

print(f'Render started with PID: {p.pid}')
