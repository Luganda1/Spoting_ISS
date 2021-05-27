import requests
import datetime as dt
import smtplib
import time

MY_LAT = 34.019455
MY_LNG = -118.491188
gmail = "mugomugowa@gmail.com"
password = "5190333t"


def iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()["iss_position"]

    latitude = float(data["latitude"])
    longitude = float(data["longitude"])

    if (MY_LAT - 5) <= latitude <= (MY_LAT + 5) and (MY_LNG - 5) <= longitude <= (MY_LNG + 5):
        return True


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LNG,
        "formatted": 0,
    }

    response_sun = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    response_sun.raise_for_status()
    data_sun = response_sun.json()

    sunrise = data_sun["results"]["sunrise"]
    sunset = data_sun["results"]["sunset"]
    sunrise = int(sunrise.split("T")[1].split(":")[0])
    sunset = int(sunset.split("T")[1].split(":")[0])

    time_now = dt.datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True


# if the iss is close to my current location
# and the time of the day is dark
# them send me an email to tell me to look up

while True:
    time.sleep(60)
    if iss_overhead() and is_night():
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=gmail, password=password)
            connection.sendmail(
                from_addr=gmail,
                to_addrs="rugant4@gmail.com",
                msg="Subject: Check the skies now\n\n The international space station is passing by right now"
            )


