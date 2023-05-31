
def pid_status(pid, df):
    if not pid in df['Participant'].values:
        print(f'Adding {pid} to the table.')
        new_row = [pid] + [0] * (df.shape[1] - 1)
        df.loc[len(df)] = new_row
    # else:
    #     print(f'{pid} alredy exists in the table.')
    return df