# esp8266 hourly deep sleep for multiple increments
Micropython library that enables multiple hourly increments of deep sleep.


# Problem statement
By default micropython can sleep up to 71 minutes. This creates a problem
when one needs code to run once every day or even longer.

# Solution
This library is an easy and unintrusive way to run some code once every a
long window of hours. The way it works is that it deep sleeps the board for
an hour and upon waking checks the state of the RTC memory where it keeps an
increment.

# Usage

# boot.py
    from library import HourlySleeper
    # we instantiate the sleeper with the hours that we want it to sleep after
    # the first execution of our code.
    hourly_sleeper = HourlySleeper(24)

   and that is all its needed in boot.py

# main.py
    import machine
    import time


    def main():
        try:
            hourly_sleeper()

            # here is where our code would be
            # we need the reset after our code so we enter the deep sleep loop

            machine.reset()
        except Exception:
            machine.reset()

    if __name__ == '__main__':
        main()

# Resetting the counter

If we need to reset the counter we need to hard reset the board through the
reset button. Its best to try a couple of times to make sure that the signal
is properly caught.


# Debugging

In order to debug our code and the loop we can set

    HOURLY_SLEEP_DEBUG=True

either in boot.py or in main.py
If that variable is set the deepsleep performed is 6 seconds long instead of
an hour to make the monitoring a bit more manageable.