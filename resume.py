import os
import subprocess
import argparse

# Define arguments
parser = argparse.ArgumentParser()
parser.add_argument('--size', nargs=2, type=float, default=[0.5, 1.3], help='Range of scaling factor to try')
args = parser.parse_args()

# Check for xpdf
if not os.path.exists('/usr/local/bin/pdftotext'):
    print("xpdf is not installed. Please install it using 'brew install xpdf' on Mac or 'sudo apt-get install xpdf' on Linux.")
    exit()

# Run compile.py with scaling factor in range
for scale in reversed(range(int(args.size[0] * 100), int(args.size[1] * 100) + 1)):
    print(f"Trying scale factor: {scale/100}")
    subprocess.run(['python3', 'compile.py', '--size', str(scale/100)], stdout=subprocess.PIPE)
    # Check if resulting PDF is one page
    out = subprocess.check_output(['/usr/local/bin/pdftotext', '-enc', 'UTF-8', '-f', '1', '-l', '1', 'resume.pdf', '-'])
    num_pages = len(out.split(b'\f'))  # Count number of form feeds (page breaks)
    if num_pages == 1:
        print("Success! Only one page.")
        break
    print(f"Number of pages: {num_pages}")
