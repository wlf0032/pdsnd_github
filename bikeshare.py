import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'nyc': 'new_york_city.csv',
              'washington': 'washington.csv' }
cities = ['chicago','new york city','nyc','washington']
months = ['all','january', 'february','march','april','may','june']
days = ['all','monday', 'tuesday','wednesday','thursday','friday','saturday','sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    global city, month, day

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city =  input('From the following: chicago, new york city/nyc, washington], please type in the city you are interested in:')
    city = city.lower()
    while city not in cities:
        city = input('Please check your spelling, and try again:')
        city = city.lower()

    # TO DO: get user input for month (all, january, february, ... , june)
    month =  input('From the following: [all, january, february... june], please type in the month you are interested in:')
    month = month.lower()
    while month not in months:
        month = input('Please check your spelling, and try again:')
        month = month.lower()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day =  input('From the following: [all, monday, tuesday... sunday], please type in the day you are interested in:')
    day = day.lower()
    while day not in days:
        day = input('Please check your spelling, and try again:')
        day = day.lower()

    print('-'*40)
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
    df = pd.read_csv(CITY_DATA.get(city))
    df['Start Time'] = pd.to_datetime(df['Start Time'])     # convert the Start Time column to datetime
    df['month'] = df['Start Time'].dt.month                 # extract month and day of week from Start Time to create new columns
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':                              # filter by month if applicable
        month = months.index(month)                 # use the index of the months list to get the corresponding int
        df = df[df['month']==month]                 # filter by month to create the new dataframe

    if day != 'all':                                # filter by day of week if applicable
        df = df[df['day_of_week'] == day.title()]   # filter by day of week to create the new dataframe

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    if month == 'all':                                              # TO display the most common month
        commmonth = df['month'].mode()[0]
        print('\nThe most common month is {}'.format(commmonth))
    else:
        print('\nYou have only chosen {}'.format(month))

    if day == 'all':                                                # TO display the most common day of week
        commday = df['day_of_week'].mode()[0]
        print('\nThe most common day of the week is {}'.format(commday))
    else:
        print('\nYou have only chosen {}'.format(day))

    commhour = df['hour'].mode()[0]                                 # TO display the most common start hour
    print('\nThe most common hour is from {} to {} o"clock'.format(commhour,(commhour+1)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    commststaion = df['Start Station'].mode()[0]     # display most commonly used start station
    commendstaion = df['End Station'].mode()[0]      # display most commonly used end station
    df['stationcomb'] = df['Start Station'].str.cat(df['End Station'], sep=' -> ')
    commcomb = df['stationcomb'].mode()[0]           # display most frequent combination of start station and end station trip
    
    print('\nThe most commonly used start station is: {}'.format(commststaion))
    print('\nThe most commonly used end station is: {}'.format(commendstaion))
    print('\nThe most commonly used start/end station combo is: {}'.format(commcomb))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    dursum = round(df['Trip Duration'].sum()/3600,1)        # TO display total travel time in hours
    durmean = round(df['Trip Duration'].mean()/60,1)        # TO display mean travel time in minutes
    
    print('The total travel time is: {} hours, and mean travel time is: {} minutes'.format(dursum,durmean))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    typecount = pd.DataFrame(df['User Type'].value_counts())     # TO Display counts of user types
    print('Count of each user type is: \n',typecount)  

    if city == 'washington':
        print('Washington doesn"t have user gender and birth year data')
    else:
        gendercount = pd.DataFrame(df['Gender'].value_counts())        # TO Display counts of gender
        dobmin = int(df['Birth Year'].min())                           # TO DO: Display earliest
        dobmax = int(df['Birth Year'].max())                           # most recent, and most common year of birth
        dobmode =int(df['Birth Year'].mode()[0])                         

        print('Count of each genter type is: \n',gendercount)
        print('The oldest, youngest and most common year of birth are respectively {},{}, and {}'.format(dobmin,dobmax,dobmode))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def display_raw_data(df):
    showdata = input('Do you want to see the raw data (Y/N)?').lower()

    while showdata not in ['y','yes','n','no']:
        showdata = input('Invalid input, please re-enter (Y/N)?').lower()

    n = 0
    while showdata in ['y','yes']:
        print(df[n:n+5])
        n += 5
        showdata = input('Show anothter 5 rows (Y/N)?').lower()

    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() not in ['y','yes']:
            break


if __name__ == "__main__":
	main()
