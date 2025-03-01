import sys
import os
import shutil
from tqdm import tqdm


if __name__ == '__main__':
    input_path = sys.argv[1]
    output_path = sys.argv[2]

    times = os.listdir(input_path)

    for t in tqdm(times):
        if t.startswith('.'):
            continue

        sn = os.listdir(os.path.join(input_path, t))
        sn = [s for s in sn if not s.startswith('.')][0]
        folder = os.path.join(input_path, t, sn, 'origin', '11')
        filename = os.listdir(folder)
        filename = [f for f in filename if not f.startswith('.')][0]

        shutil.copyfile(os.path.join(folder, filename), os.path.join(output_path, filename))
        pass
    pass