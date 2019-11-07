from sys import stdout

def showProgress(iter_ix, num_iters, bar_len=49):
    '''
    Print progress bar with percentage.
    Arguments:
        iter_ix (int): iteration index (zero-based).
        num_iters (int): total number of iterations.
        bar_len (int): bar length.
    '''
    i = iter_ix + 1
    progress = float(i) / num_iters
    arrow_len = int(round((bar_len * progress)))
    percent = str(int(round(100 * progress))).zfill(2)
    stdout.write('\r[{0}>{1}] {2}% ({3} of {4})'.format('-' * arrow_len, ' ' * (bar_len - arrow_len), percent, str(i), str(num_iters)))
    stdout.flush()
    if i == num_iters:
        print('\n')
