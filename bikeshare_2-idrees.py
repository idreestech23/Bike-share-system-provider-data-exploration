import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
cities = ['chicago', 'new york city', 'washington']
months = ["january", "february", "march", "april", "may", "June"]
days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]



def get_filters():
    """
        Asks user to specify a city, month, and day to analyze.

        Returns:
        (str) city - name of the city to analyze
        (str) month - An integer representing a month. ==> (1 = january)...(6 = june)
        (str) day - An integer representing a day in the week. ==> (1 = monday)...(7 = sunday)
        note: The function returns 0 as a value for all days or all months.
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Choose a City from [chicago, new york city, washington]: ").strip().lower()
        if city in cities:
            break
        else:
            print("Invalid input, please choose one from the specified options and make sure the spelling is correct.")

    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = int(input("choose a month by entering an integer from 1 to 6 (1 = january)...(6 = june) or enter 0 for all: ").strip())
            if int(month) in [0,1,2,3,4,5,6]:
                break
            else:
                print("Invalid input, please choose one from the specified options.")
        except:
            print("Invalid input, please inter an intger.")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = int(input("choose a day by entering an integer from 1 to 7 (1 = monday)...(7 = sunday) or enter 0 for all: ").strip())
            if int(day) in [0,1,2,3,4,5,6,7]:
                break
            else:
                print("Invalid input, please choose one from the specified options.")
        except:
            print("Invalid input, please inter an intger.")
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - An integer representing a month. ==> (1 = january)...(6 = june)
        (str) day - An integer representing a day in the week. ==> (1 = monday)...(7 = sunday)
        note: The function accepts 0 as a value for all days or all months.
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    df["trip"] = "(" + df["Start Station"] +") to (" + df["End Station"] + ")"

    if month == 0 and day == 0:
        return df
    if day > 0 and day <= 7:
        df = df[df['day_of_week'] == day-1]

    if month > 0 and month <= 6:
        df = df[df['month'] == month]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    print("")
    start_time = time.time()


    # display the most common month
    print("The most common month: "+months[df['month'].mode()[0]-1].title())

    # display the most common day of week
    print("The most common day of week: "+ days[df['day_of_week'].mode()[0]].title())

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print("The most common start hour: "+ str(df['hour'].mode()[0]))
    print("")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    print("")
    start_time = time.time()

    # display most commonly used start station
    print("Most commonly used start station: "+ df["Start Station"].mode()[0])

    # display most commonly used end station
    print("Most commonly used end station: "+ df["End Station"].mode()[0])

    # display most frequent combination of start station and end station trip
    print("Most frequent combination of start station and end station trip " + df["trip"].mode()[0])
    print("")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    print("")
    start_time = time.time()

    # display total travel time
    print("Total travel time: " + str(df["Trip Duration"].sum()))
    # display mean travel time
    print("Mean travel time: " + str(df["Trip Duration"].mean()))
    print("")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    print("")
    start_time = time.time()

    # Display counts of user types
    print(df["User Type"].value_counts())
    print("")
    # Display counts of gender
    try:
        print(df["Gender"].value_counts())
    except:
        print("No data for gender.")
    print("")
    # Display earliest, most recent, and most common year of birth
    try:
        print("Earlist date of birth: "+ str(df["Birth Year"].min()))
        print("Most recent date of birth: "+ str(df["Birth Year"].max()))
        print("Most common date of birth: "+ str(df["Birth Year"].mode()))
    except:
        print("No data for birth date.")
    print("")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)




def main():
    while True:
        city, month, day = get_filters()
        print("The data selected is for:")
        print("- "+ city.title()+" city.")
        if month == 0:
            print("- All months.")
        else:
            print("- The month of "+ months[month-1]+".")
        if day == 0:
            print("- All days of week")
        else:
            print("- Only " + days[day-1]+"s.")
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        line = 0
        while True:
            print_lines = input("Would you like to print the next 5 lines? Enter yes or no.\n").strip().lower()
            if print_lines == "yes":
                if df.shape[0] - line >= 5:
                    print("")
                    print(df[line:line+5])
                    line += 5
                    print("")
                    print(f"Lines {line} to {line+5} printed.")
                    print("")
                else:
                    print("")
                    print(df[line:])
                    print("")
                    print(f"Lines {line} to {df.shape[0]} printed.")
                    print("")
                    break
            else:
                break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
