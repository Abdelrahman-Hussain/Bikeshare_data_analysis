import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_list = ['chicago', 'new york city', 'washington']
    city = ''
    first_input = True
    while city not in city_list:
        if not first_input:
            print('Wrong input try again !')
        city = input('Enter the city name: ').lower()
        first_input = False

    # get user input for month (all, january, february, ... , june)
    month_list = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    month = ''
    first_input = True
    while month not in month_list:
        if not first_input:
            print('Wrong input try again !')
        month = input('Enter month name: ').lower()
        first_input = False

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day_list = ['all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
    day = ''
    first_input = True
    while day not in day_list:
        if not first_input:
            print('Wrong input try again !')
        day = input('Enter week day: ').lower()
        first_input = False
    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    # weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df.loc[df['month'] == month]

        # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df.loc[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    new_df = df.copy(deep=True)
    new_df['Start Time'] = pd.to_datetime(new_df['Start Time'])

    # display the most common month
    new_df['month'] = new_df['Start Time'].dt.month
    popular_month = new_df['month'].mode()[0]
    print('The most popular day in the month: ', popular_month)

    # display the most common day of week
    new_df['day_of_week'] = new_df['Start Time'].dt.day_name()
    popular_week_day = new_df['day_of_week'].mode()[0]
    print('The most popular day in the week: ', popular_week_day)

    # display the most common start hour
    new_df['hour'] = new_df['Start Time'].dt.hour
    popular_hour = new_df['hour'].mode()[0]
    print('The most popular hour: ', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('The most popular start station: ', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('The most popular end station: ', popular_end_station)

    # display most frequent combination of start station and end station trip
    new_df = df.copy(deep=True)
    new_df['start_end_station'] = ('FROM ' + new_df['Start Station'] + ' TO ' + new_df['End Station'])
    popular_start_end_station = new_df['start_end_station'].mode()[0]
    print('The most popular start and end station: ', popular_start_end_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('total travel time : ', total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('mean travel time : ', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(df['User Type'].value_counts(), '\n')

    if 'Gender' in df:
        # Display counts of gender
        print(df['Gender'].value_counts(), '\n')

        # Display earliest, most recent, and most common year of birth
        print('The earliest year of birth', df['Birth Year'].min())
        print('The most recent year of birth', df['Birth Year'].max())
        print('The most common year of birth', df['Birth Year'].mode())
    else:
        print('There is no gender nor Birth Year data in washington')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    while True:
        try:
            city, month, day = get_filters()
            df = load_data(city, month, day)
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
        except:
            print('Wrong input !')
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
