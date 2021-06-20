import time

import pandas as pd

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
    city_options = ['chicago', 'new york city', 'washington']
    month_options = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    day_options = ['all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Pick a city amongst chicago, new york city, washington').lower()
    while city not in city_options:
        city = input('Pick a city amongst chicago, new york city, washington').lower()

    # get user input for month (all, january, february, ... , june)

    month = input('Pick a month amongst all, january, february, march, april, may, june').lower()
    while month not in month_options:
        month = input('Pick a month amongst all, january, february, march, april, may, june').lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Pick a day amongst all, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday').lower()
    while day not in day_options:
        day = input('Pick a day amongst all, sunday, monday, tuesday, wednesday, thursday, friday, saturday').lower()

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
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df_temp = pd.read_csv(CITY_DATA[city])

    df_temp["Start Time"] = pd.to_datetime(df_temp["Start Time"])
    df_temp["End Time"] = pd.to_datetime(df_temp["End Time"])

    month_get = df_temp["Start Time"].dt.month_name()
    day_get = df_temp["Start Time"].dt.day_name()
    hour_get = df_temp["Start Time"].dt.hour

    df_temp["month_get"] = month_get.str.lower()
    df_temp["day_get"] = day_get.str.lower()
    df_temp["hour_get"] = hour_get

    day_list = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
    month_list = ['january', 'february', 'march', 'april', 'may', 'june']

    if day == 'all':
        day_mask = df_temp.day_get.isin(day_list)
    else:
        day_mask = df_temp.day_get == day

    if month == 'all':
        month_mask = df_temp.month_get.isin(month_list)
    else:
        month_mask = df_temp.month_get == month

    df = df_temp.loc[day_mask & month_mask]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    frequent_month = df.month_get.mode()

    # display the most common day of week
    frequent_day = df.day_get.mode()

    # display the most common start hour
    frequent_hour = df.hour_get.mode()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("\n the most common month: \t")
    print(frequent_month)
    print("\n the most common day of the week: \t")
    print(frequent_day)
    print("\n the most common start hour: \t")
    print(frequent_hour)
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    frequent_start = df["Start Station"].mode()

    # display most commonly used end station
    frequent_end = df["End Station"].mode()

    # display most frequent combination of start station and end station trip
    start_end = df["Start Station"] + " TO " + df["End Station"]
    start_end = start_end.mode()

    print("\nThis took %s seconds." % (time.time() - start_time))

    print("\nmost commonly used start station: ")
    print(frequent_start)

    print("\nmost commonly used end station: ")
    print(frequent_end)
    print("\nmost frequent combination of start station and end station trip: ")
    print(start_end)
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    duration_travel = df["End Time"] - df["Start Time"]
    df['duration_travel'] = duration_travel.dt.total_seconds()
    total_duration_travel = duration_travel.sum()

    # display mean travel time
    duration_travel_mean = duration_travel.mean()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("\ntotal travel time: ")
    print(total_duration_travel)
    print("\nmean travel time: ")
    print(duration_travel_mean)
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    global common_yr, max_yr, min_yr, gender_count
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df["User Type"].value_counts()

    if 'Gender' in df.columns:
        Gender_Check = "OK"
        # Display counts of gender
        gender_count = df["Gender"].value_counts()
    else:
        Gender_Check = "Nok"

    if 'Birth Year' in df.columns:
        Year_Check = "OK"
        # Display earliest, most recent, and most common year of birth
        min_yr = df["Birth Year"].min(skipna=True)
        max_yr = df["Birth Year"].max(skipna=True)
        common_yr = df["Birth Year"].mode()
    else:
        Year_Check = "NOK"

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("\ncounts of user types: ")
    print(user_type)

    if Gender_Check == "OK":
        print("\ncounts of gender: ")
        print(gender_count)
    else:
        print("No Gender Data")

    if Year_Check == "OK":
        print("\nearliest year of birth: ")
        print(min_yr)
        print("\nmost recent year of birth: ")
        print(max_yr)
        print("\nmost common year of birth: ")
        print(common_yr)
    else:
        print("No Birth Year Data")
    print('-' * 40)

def get_more(df):
    n1=0
    n2=5
    data_show = input('\nWould you like to see some raw data - Say Yes or No.\n').lower()
    while data_show=='yes':
        print(df.iloc[n1:n2,:])
        n1=n1+5
        n2=n2+5
        data_show = input('\nWould you like to see some raw data - Say Yes or No.\n').lower()
    print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        get_more(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
