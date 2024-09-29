import argparse
import string
import time
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from loguru import logger

def count_characters(file_path, plot_histogram, marker=None, end_marker=None):
    counts = Counter()
    total_chars = 0
    total_words = 0
    total_lines = 0
    in_book_content = marker is None

    with open(file_path, 'r') as input_file:
        logger.debug(f'Reading input data from {file_path}...')
        for line in input_file:
            total_lines += 1
            if marker and marker in line:
                in_book_content = True
                continue
            if end_marker and end_marker in line:
                break
            if in_book_content:
                line = line.lower()
                counts.update(char for char in line if char in string.ascii_lowercase)
                total_chars += len(line)
                total_words += len(line.split())

    logger.info(f'Character counts: {counts}')
    num_characters = sum(counts.values())
    logger.info(f'Total number of characters: {num_characters}')
    
    frequencies = {char: count / num_characters for char, count in counts.items()}
    logger.info(f'Character frequencies: {frequencies}')

    if plot_histogram:
        # Set the style
        sns.set_style("whitegrid")
        sns.set_palette("deep")

        # Create a DataFrame for easier plotting
        df = pd.DataFrame(list(frequencies.items()), columns=['Character', 'Frequency'])
        df = df.sort_values('Character')

        # Normalize the frequencies
        df['Normalized'] = (df['Frequency'] - df['Frequency'].min()) / (df['Frequency'].max() - df['Frequency'].min())

        # Create the plot with two subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 16), height_ratios=[1, 1])
        fig.subplots_adjust(hspace=0.3)  # Adjust space between subplots

        # Plot the original frequencies
        sns.barplot(x='Character', y='Frequency', data=df, ax=ax1)
        ax1.set_title('Character Frequencies in Text', fontsize=20, fontweight='bold', pad=20)
        ax1.set_xlabel('Characters', fontsize=14, labelpad=10)
        ax1.set_ylabel('Frequency', fontsize=14, labelpad=10)

        # Add value labels on top of each bar for the first plot
        for i, v in enumerate(df['Frequency']):
            ax1.text(i, v, f'{v:.4f}', ha='center', va='bottom', fontsize=8, rotation=90)

        # Plot the normalized frequencies with military green color
        military_green = '#4b5320'  # Military green color code
        sns.barplot(x='Character', y='Normalized', data=df, ax=ax2, color=military_green)
        ax2.set_title('Normalized Character Frequencies', fontsize=20, fontweight='bold', pad=20)
        ax2.set_xlabel('Characters', fontsize=14, labelpad=10)
        ax2.set_ylabel('Normalized Frequency', fontsize=14, labelpad=10)

        # Add value labels on top of each bar for the second plot
        for i, v in enumerate(df['Normalized']):
            ax2.text(i, v, f'{v:.4f}', ha='center', va='bottom', fontsize=8, rotation=90)

        # Remove top and right spines
        sns.despine()

        # Adjust layout and display the plot
        plt.tight_layout()
        plt.show()

    return frequencies, total_chars, total_words, total_lines

def print_stats(total_chars, total_words, total_lines):
    logger.info(f'Total characters: {total_chars}')
    logger.info(f'Total words: {total_words}')
    logger.info(f'Total lines: {total_lines}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Analyze character frequencies in a text file')
    parser.add_argument('file', help='Path to the input text file')
    parser.add_argument('--histogram', action='store_true', help='Plot a histogram of the character frequencies')
    parser.add_argument('--start', help='Start marker for book content')
    parser.add_argument('--end', help='End marker for book content')
    parser.add_argument('--stats', action='store_true', help='Print basic book statistics')
    args = parser.parse_args()

    start_time = time.time()
    frequencies, total_chars, total_words, total_lines = count_characters(args.file, args.histogram, args.start, args.end)
    
    if args.stats:
        print_stats(total_chars, total_words, total_lines)

    end_time = time.time()
    logger.info(f'Total elapsed time: {end_time - start_time:.2f} seconds')