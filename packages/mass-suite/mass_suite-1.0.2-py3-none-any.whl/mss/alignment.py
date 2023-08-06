import pandas as pd
import numpy as np
from tqdm import tqdm
import os
"""This file contains the functions needed to correct the peak positions
of different samples accumulated in one day's worth of analysis."""


def stack(batch_path):
    """This function compiles all samples files into one dataframe
    for analysis. It takes in files that are of the .txt type."""
    all_samples = []
    # Calculating the number of files in path
    num_files = len([f for f in os.listdir(batch_path)if
                    os.path.isfile(os.path.join(batch_path, f))])
    print("Reading in files...")
    # Reading in files into a list
    for files in range(num_files):
        sample = os.listdir(batch_path)[files]
        sample_df = pd.read_csv(batch_path + sample,
                                dtype=np.float32)
        sample_df = sample_df.drop([sample_df.columns[0]], axis=1)
        all_samples += [sample_df]
    # Combining all the dataframes into one
    total_samples = pd.concat(all_samples)
    all_samples.clear()
    # Cleaning up the data before processing
    total_samples.loc[total_samples.sn == 0, 'sn'] = float('inf')
    total_samples.loc[total_samples.score == 3.0, 'score'] = 0.1
    total_samples.loc[total_samples.score == 2.0, 'score'] = 0.6
    print("Process completed!")
    return num_files, total_samples


def realignment(batch_path, batch_name, file_type, rt_error, MZ_error):
    """This function works by using one .txt file as a reference in which
    other files realigned to in terms of precursor and RT. """
    RT_error = rt_error  # units of minutes, can be adjusted
    alignment_df = pd.DataFrame()
    mz_error = MZ_error
    standard_sample = os.listdir(batch_path)[0]  # first sample
    # reads .txt file into a dataframe
    standard_df = pd.read_csv(batch_path + standard_sample, usecols=['rt',
                              'm/z', 'sn', 'score', 'peak area'],
                              dtype=np.float32)
    # Creating the reference df based off 1st sample
    alignment_df['m/z'] = standard_df.iloc[:, 0]
    alignment_df['rt'] = standard_df.iloc[:, 1]
    alignment_df['sn'] = standard_df.iloc[:, 2]
    alignment_df['score'] = standard_df.iloc[:, 3]
    alignment_df['Sum RT (min)'] = 0.0
    alignment_df['Sum Precursor m/z'] = 0.0
    alignment_df['Sum sn'] = 0.0
    alignment_df['Sum score'] = 0.0
    alignment_df['Sum RT (min)'] = alignment_df[
                                   'Sum RT (min)'].astype('float32')
    alignment_df['Sum Precursor m/z'] = alignment_df[
                                        'Sum Precursor m/z'].astype('float32')
    alignment_df['Sum sn'] = alignment_df['Sum sn'].astype('float32')
    alignment_df['Sum score'] = alignment_df['Sum score'].astype('float32')
    alignment_df.loc[alignment_df.sn == 0, 'sn'] = float('inf')
    alignment_df.loc[alignment_df.score == 3.0, 'score'] = 0.1
    alignment_df.loc[alignment_df.score == 2.0, 'score'] = 0.6
    # col_index to track where to add sample columns
    col_index = 8
    num_files, total_samp = stack(batch_path)
    for files in range(num_files):
        sample = os.listdir(batch_path)[files]  # Creates file columns
        sample = sample[:-4]  # removes extension part in sample name
        alignment_df[sample] = 0.0
        alignment_df[sample] = alignment_df[sample].astype('float32')
    print("Initial reference built")
    print("Alignment beginning..")
    for row in tqdm(range(len(total_samp))):
        if alignment_df.isnull().values.any() is True:
            alignment_df = alignment_df.fillna(0)
        else:
            pass
        row_max = len(alignment_df)
        if row < range(len(total_samp))[-1]:
            # Loops until a change in sample occurs by index
            if total_samp.index[row] < total_samp.index[row + 1]:
                # checks to see if row exists in reference or not
                overlap = np.where(((alignment_df.iloc[:, 1] - RT_error)
                                   <= total_samp.iloc[row, 1]) &
                                   (total_samp.iloc[row, 1] <=
                                   (alignment_df.iloc[:, 1] + RT_error))
                                   & ((alignment_df.iloc[:, 0] - mz_error)
                                      <= total_samp.iloc[row, 0])
                                   & (total_samp.iloc[row, 0] <=
                                       (alignment_df.iloc[:, 0] + mz_error)))
                if len(overlap[0]) > 0:
                    overlap = [overlap][0][0][0]
                    # checks for any duplicates
                    if (alignment_df.iloc[overlap, col_index]) > 0:
                        alignment_df.at[overlap, alignment_df.columns[
                                        col_index]] += total_samp.iloc[row, 4]
                        # Averages the mean if there is a repeat intensity
                        alignment_df.at[overlap, alignment_df.columns[
                                         col_index]] /= 2
                    else:
                        # sets intensity value where realignment was identified
                        alignment_df.at[overlap, alignment_df.columns[
                                             col_index]] = total_samp.iloc[
                                                           row, 4]
                        # adds rt, sn, m/z, score to aligned point
                        alignment_df.at[overlap,
                                        'Sum RT (min)'] += (total_samp.
                                                            iloc[row, 1])
                        alignment_df.at[overlap,
                                        'Sum Precursor m/z'] += (total_samp.
                                                                 iloc[row, 0])
                        alignment_df.at[overlap, 'Sum sn'] += (total_samp.
                                                               iloc[row, 2])
                        alignment_df.at[overlap, 'Sum score'] += (total_samp.
                                                                  iloc[row, 3])
                else:
                    # appends as a new reference if nothing is found
                    alignment_df.loc[row_max] = total_samp.iloc[row, 0:4]
                    alignment_df.at[alignment_df.index[
                                   -1], alignment_df.columns[
                                        col_index]] = total_samp.iloc[row, 4]
                    alignment_df.at[alignment_df.index[
                                   -1], 'Sum RT (min)'] = total_samp.iloc[
                                                          row, 1]
                    alignment_df.at[alignment_df.index[
                                   -1], 'Sum Precursor m/z'] = total_samp.iloc[
                                                               row, 0]
                    alignment_df.at[alignment_df.index[
                                   -1], 'Sum sn'] = total_samp.iloc[row, 2]
                    alignment_df.at[alignment_df.index[
                                   -1], 'Sum score'] = total_samp.iloc[row, 3]
            else:
                # if index changes, moves to next sample column
                col_index += 1
                overlap = np.where(((alignment_df.iloc[:, 1] - RT_error)
                                   <= total_samp.iloc[row, 1]) &
                                   (total_samp.iloc[row, 1] <=
                                   (alignment_df.iloc[:, 1] + RT_error))
                                   & ((alignment_df.iloc[:, 0] - mz_error)
                                      <= total_samp.iloc[row, 0])
                                   & (total_samp.iloc[row, 0] <=
                                       (alignment_df.iloc[:, 0] + mz_error)))
                if len(overlap[0]) > 0:
                    overlap = [overlap][0][0][0]
                    if (alignment_df.iloc[overlap, col_index]) > 0:
                        alignment_df.at[overlap, alignment_df.columns[
                                         col_index]] += total_samp.iloc[row, 4]
                        # Averages the mean if there is a repeat intensity
                        alignment_df.at[overlap, alignment_df.columns[
                                         col_index]] /= 2
                    else:
                        alignment_df.at[overlap, alignment_df.columns[
                                             col_index]] = total_samp.iloc[
                                                           row, 4]
                        # adds rt, m/z, score, sn to aligned point
                        alignment_df.at[overlap,
                                        'Sum RT (min)'] += (total_samp.
                                                            iloc[row, 1])
                        alignment_df.at[overlap,
                                        'Sum Precursor m/z'] += (total_samp.
                                                                 iloc[row, 0])
                        alignment_df.at[overlap, 'Sum sn'] += (total_samp.
                                                               iloc[row, 2])
                        alignment_df.at[overlap, 'Sum score'] += (total_samp.
                                                                  iloc[row, 3])
                else:
                    # appends as a new reference if nothing is found
                    alignment_df.loc[row_max] = total_samp.iloc[row, 0:4]
                    alignment_df.at[alignment_df.index[
                                   -1], alignment_df.columns[
                                        col_index]] = total_samp.iloc[row, 4]
                    alignment_df.at[alignment_df.index[
                                   -1], 'Sum RT (min)'] = total_samp.iloc[
                                                          row, 1]
                    alignment_df.at[alignment_df.index[
                                   -1], 'Sum Precursor m/z'] = total_samp.iloc[
                                                               row, 0]
                    alignment_df.at[alignment_df.index[
                                   -1], 'Sum sn'] = total_samp.iloc[row, 2]
                    alignment_df.at[alignment_df.index[
                                   -1], 'Sum score'] = total_samp.iloc[row, 3]
        else:  # for last row of dataframe
            overlap = np.where(((alignment_df.iloc[:, 1] - RT_error)
                               <= total_samp.iloc[row, 1]) &
                               (total_samp.iloc[row, 1] <=
                                (alignment_df.iloc[:, 1] + RT_error))
                               & ((alignment_df.iloc[:, 0] - mz_error)
                                   <= total_samp.iloc[row, 0])
                               & (total_samp.iloc[row, 0]
                                   <= (alignment_df.iloc[:, 0] + mz_error)))
            if len(overlap[0]) > 0:
                overlap = [overlap][0][0][0]
                if (alignment_df.iloc[overlap, col_index]) > 0:
                    alignment_df.at[overlap, alignment_df.columns[
                                         col_index]] += total_samp.iloc[row, 4]
                    # Averages the mean if there is a repeat intensity
                    alignment_df.at[overlap, alignment_df.columns[
                                         col_index]] /= 2
                else:
                    # sets intensity value where realignment was identified
                    alignment_df.at[overlap, alignment_df.columns[
                                         col_index]] = total_samp.iloc[row, 4]
                    # adds rt, m/z, score, sn to aligned point
                    alignment_df.at[overlap, 'Sum RT (min)'] += (total_samp.
                                                                 iloc[row, 1])
                    alignment_df.at[overlap,
                                    'Sum Precursor m/z'] += (total_samp.
                                                             iloc[row, 0])
                    alignment_df.at[overlap, 'Sum sn'] += total_samp.iloc[
                                                           row, 2]
                    alignment_df.at[overlap, 'Sum score'] += total_samp.iloc[
                                                              row, 3]
            else:
                # appends as a new reference if nothing is found
                alignment_df.loc[row_max] = total_samp.iloc[row, 0:4]
                alignment_df.at[alignment_df.index[
                               -1], alignment_df.columns[
                                    col_index]] = total_samp.iloc[row, 4]
                alignment_df.at[alignment_df.index[
                               -1], 'Sum RT (min)'] = total_samp.iloc[row, 1]
                alignment_df.at[alignment_df.index[
                               -1], 'Sum Precursor m/z'] = total_samp.iloc[
                                                           row, 0]
                alignment_df.at[alignment_df.index[
                               -1], 'Sum sn'] = total_samp.iloc[row, 2]
                alignment_df.at[alignment_df.index[
                               -1], 'Sum score'] = total_samp.iloc[row, 3]
    alignment_df.rename(columns={'rt': 'Average RT (min)'}, inplace=True)
    alignment_df.rename(columns={'m/z': 'Average m/z'}, inplace=True)
    alignment_df.rename(columns={'sn': 'Average sn'}, inplace=True)
    alignment_df.rename(columns={'score': 'Average score'}, inplace=True)
    # Replace all NaN elements with 0
    alignment_df = alignment_df.fillna(0)
    # final dataframe sorted by m/z
    alignment_df = alignment_df.sort_values(by='Average m/z',
                                            ignore_index=True)
    # empty list to hold invalid peaks
    invalid = []
    for rows in range(len(alignment_df)):
        # Calculating the averages after the iterations
        # requires count of nonzero count to calculate the mean properly
        count = np.count_nonzero(alignment_df.iloc[rows, 8:])
        if count > 0:
            alignment_df.at[rows, 'Average RT (min)'] = (alignment_df.loc[rows,
                                                         'Sum RT (min)']/count)
            alignment_df.at[rows, 'Average m/z'] = (alignment_df.loc[rows,
                                                    'Sum Precursor m/z']/count)
            alignment_df.at[rows, 'Average sn'] = (alignment_df.loc[rows,
                                                   'Sum sn']/count)
            alignment_df.at[rows, 'Average score'] = (alignment_df.loc[rows,
                                                      'Sum score']/count)
        else:
            invalid.append(rows)
            print("Identified invalid peak(s)")  # For detection error
    if len(invalid) > 0:
        for i in range(len(invalid)):
            alignment_df = alignment_df.drop(alignment_df.index[invalid[i]])
        alignment_df = alignment_df.reset_index(drop=True)
        print("Removed invalid peak(s) from reference")
    else:
        pass
    # Drop columns to collect sums for averaging
    alignment_df = alignment_df.drop(columns=[
                   'Sum RT (min)', 'Sum Precursor m/z',
                   'Sum sn', 'Sum score'])
    # rounds numbers in the first two columns
    alignment_df = alignment_df.round({'Average RT (min)': 3,
                                       'Average m/z': 5})
    print("Alignment done!")
    # converts file for saving
    alignment_df.to_csv(batch_path + batch_name +
                        file_type, header=True, index=False)
    print("File saved")
    return alignment_df
