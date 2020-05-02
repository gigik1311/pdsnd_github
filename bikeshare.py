import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """ Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data! When entering your answer to each question, please make sure that your input uses the correct spacing. ')
    # Gets a city from the user
    while True:
        try:
            city = input('Choose from these cities: chicago, new york city, washington: ')
            if city in CITY_DATA:
                print('Great!')
                print('You have chosen {}.'.format(city))
                break
            elif city not in CITY_DATA:
                print('Please input a one of the cities (chicago, new york city, washington) and try again.')
        except NameError:
            print('Please input a one of the cities (chicago, new york city, washington) and try again.')
    # Gets a month from the user
    while True:
        try:
            months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
            month = input('Choose the month you want to see (january - june) or choose "all": ')
            if month in months:
                print('Great!')
                print('You have chosen {}.'.format(month))
                break
            elif month not in months:
                print('Please try again. Input a month (january - june) or choose "all".')
        except NameError:
            print('Please try again. Input a month (january - june) or choose "all": ')
    # Gets a day from the user
    while True:
        try:
            days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all', 'none']
            day = input('Choose the day you want to see (monday, tuesday, etc.) or choose "all": ')
            if day in days:
                print('Great!')
                print('You have chosen {}.'.format(day))
                break
            elif day_input not in days:
                print('Please try again. Input a day (monday, tuesday, etc.) or choose "all": ')
        except NameError:
            print('Please try again. Input a day (monday, tuesday, etc.) or choose "all": ')
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Arguments:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    try:
        df = pd.read_csv(CITY_DATA[city])
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df['End Time'] = pd.to_datetime(df['End Time'])
        df['month'] = df['Start Time'].dt.month
        df['day_of_week'] = df['Start Time'].dt.weekday_name
        df['hour'] = df['Start Time'].dt.hour
        if month != 'all':
            months = ['january', 'february', 'march', 'april', 'may', 'june']
            month = months.index(month) + 1
            df = df[df['month'] == month]
        if day != 'all':
            df[df['day_of_week'] == day.title()]
        return df
    except Exception as exception:
        print('Could not load the file, an error occurred: {}'.format(exception))


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start = time.time()
    try:
        most_common_month_number = df['Start Time'].dt.month.mode()[0]
        most_common_month = df['month'].mode()[0]
        print('The month with the most travelers is {}'.format(most_common_month))
    except Exception as exception:
        print('Could not calculate the most popular month, as an error occured: {}'.format(exception))
    try:
        most_common_day_of_week = df['day_of_week'].mode()[0]
        print('The day of the week with the most travelers is {}.'.format(most_common_day_of_week))
    except Exception as exception:
        print('Could not calculate the most common day of the week, as an error occured: {}'.format(exception))
    try:
        most_common_hour = df['hour'].mode()[0]
        print('The hour of the day with the most travelers is {}.'.format(most_common_hour))
    except Exception as exception:
        print('Could not calculate the most common start hour, as an error occured: {}'.format(exception))
    print("\nThis took %s seconds." % (time.time() - start))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    # Gets the most common start station based on the user's input
    most_common_start_station = df['Start Station'].mode()[0]
    print('The most common Start Station is {}.'.format(most_common_start_station))
    # Gets the most common end station based on the user's input
    most_common_end_station = df['End Station'].mode()[0]
    print('The most common End Station is {}.'.format(most_common_end_station))
    # Gets the most common start station/end station combination based on the user's input
    most_frequent_combination = df[['Start Station', 'End Station']].mode().loc[0]
    print('The most common Start Station/End Station combination is {}.'.format(most_frequent_combination))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # Gets the total duration of all trips based on user's input
    total_trip_duration = df['Trip Duration'].sum()
    print('The total trip duration is {} seconds. Which is {} minutes. Which is {} hours.'.format(total_trip_duration, total_trip_duration / 60, (total_trip_duration / 60) / 60))
    # Gets the average trip duration based on the user's input
    average_trip_duration = df['Trip Duration'].mean()
    print('The average trip duration is {} seconds. Which is {} minutes. Which is {} hours.'.format(average_trip_duration, average_trip_duration / 60, (average_trip_duration / 60) / 60))
    print('This took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # Diplays User Type based on the user's input
    if 'User Type' in df.columns:
        user_type = df['User Type'].value_counts()
        print('The full amount of each user type is {}.'.format(user_type))
    # Gets the number of each gender based on the user's input, except for Washington
    try:
        gender = df['Gender'].value_counts()
        print('The total in each gender is {}.'.format(gender))
    except:
        print('There is no gender information for Washington.\n')
    try:
        # Gets the earliest birth year based on the user's input, except for Washington
        earliest_year_of_birth = int(df['Birth Year'].min())
        print('The earliest birth year is {}.'.format(earliest_year_of_birth))
        # Gets the most recent birth year based on the user's input, except for Washington
        most_recent_year_of_birth = int(df['Birth Year'].max())
        print('The most recent birth year is {}.'.format(most_recent_year_of_birth))
        # Gets the most common birth year based on the user's input, except for Washington
        most_common_year_of_birth = int(df['Birth Year'].mode()[0])
        print('The most common birth year is {}.'.format(most_common_year_of_birth))
    except:
        print('There is no birth year information for Washington.')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# Asks if user would like to see raw data in 5 rows at a time
def display_raw_data(df):
    """Displays raw data. Prompts user and asks user if they would like to see 5 rows of data."""
    start_index = 0
    end_index = 5
    raw_data = input('Would you like to see the first 5 rows of raw data? Please choose yes or no: ').lower()
    while True:
        if raw_data == 'yes':
            print(df.iloc[start_index:end_index])
        raw_data = input('Would you like to 5 more rows of data? Please choose yes or no: ').lower()
        start_index += 5
        end_index += 5
        if raw_data == 'no':
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no: \n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
