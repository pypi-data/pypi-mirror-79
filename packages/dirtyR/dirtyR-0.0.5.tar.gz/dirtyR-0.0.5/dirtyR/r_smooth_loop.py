import glob


def r_smooth_loop(input_dir, trial_type):

    if trial_type == 'cat_alone':

        variables = [
            'x', 'y', 'cat_distance', 'velocity', 'acceleration'
        ]

    elif trial_type == 'with_owner':

        variables = [
            'x_cat', 'y_cat', 'x_owner', 'y_owner', 'distance', 'cat_distance',
            'velocity', 'acceleration'
        ]

    with open(f'smooth_{trial_type}.r', 'w') as f:

        # Load packages

        print('library(readr)\nlibrary(signal)\n', file=f)

        # Load files and create dataframes

        csv_files_dir = input_dir + '/*.csv'

        files = glob.glob(csv_files_dir)

        for file in files:

            print('\n\ndf <- read_csv("' + file + '")\n', file=f)
            print('df <- df[-c(1, 2  ), ]\n', file=f)

            # Loess

            for i in variables:
                print(i + '_loessMod' + '<- loess(' + i,
                      '~ time, data = df, span = 0.05', ')', file=f)
                print(i + '_loess05'
                       + '<- predict(' + i + '_loessMod' + ')', file=f)
                print('df$' + i + '_loess05'
                       + ' <- ' + i + '_loess05', file=f)

            print('write.csv(df, "' + file[:-4] +
                  '.csv" , row.names = FALSE)', file=f)
