import numpy as np
import scipy.misc
import time
from glob import glob
import os

def make_generator(path, n_files, batch_size):
    epoch_count = [1]
    fnames = glob(os.path.join(path, '*.jpg'))
    n_files = len(fnames)
    def get_epoch():
        images = np.zeros((batch_size, 3, 64, 64), dtype='int32')
        files = range(n_files)
        random_state = np.random.RandomState(epoch_count[0])
        random_state.shuffle(files)
        epoch_count[0] += 1
        for n, i in enumerate(files):
            image = scipy.misc.imread(fnames[i])
            images[n % batch_size] = image.transpose(2,0,1)
            if n > 0 and n % batch_size == 0:
                yield (images,)
    return get_epoch

def load(batch_size, data_dir='/home/ljw/data'):
    return (
        make_generator(data_dir+'/train', 50000, batch_size),
        make_generator(data_dir+'/valid', 49999, batch_size) if os.path.exists(data_dir+'/valid') else None
    )

if __name__ == '__main__':
    train_gen, valid_gen = load(64)
    t0 = time.time()
    for i, batch in enumerate(train_gen(), start=1):
        print "{}\t{}".format(str(time.time() - t0), batch[0][0,0,0,0])
        if i == 1000:
            break
        t0 = time.time()