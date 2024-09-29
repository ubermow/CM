
import argparse
import string
import loguru

from loguru import logger


def count_characters(file_path, plot_histogram):
    counts = {char: 0 for char in string.ascii_lowercase}
    # Rough equivalent
    # counts = {}
    # for char in string.ascii_lowercase:
    #     counts[char] = 0
    with open(file_path) as input_file:
        logger.debug(f'Reading input data from {file_path}...')
        data = input_file.read()
    logger.debug(f'Done, {len(data)} character(s) found.')
    logger.info('Counting characters...')
    for char in data.lower():
        if char in counts:
            counts[char] += 1
    logger.info(f'Character counts: {counts}')
    num_characters = sum(counts.values())
    logger.info(f'Total number of characters: {num_characters}')
    for key, value in counts.items():
        counts[key] = value / num_characters
    logger.info(f'Character frequences: {counts}')
    if plot_histogram:
        # Do something...
        pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Count the characters in a text file')
    parser.add_argument('file')
    parser.add_argument('--histogram', action='store_true',
        help='plot a histogram of the character frequencies')
    args = parser.parse_args()
    count_characters(args.file, args.histogram)
