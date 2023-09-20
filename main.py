import requests
from datetime import datetime
import time
import smtplib

MY_LAT = 50.0000 # Your latitude
MY_LONG = 30.0000 # Your longitude
MY_EMAIL = "test@email.com" # Your email
MY_PASSWORD = "wefkqjjqeqe" # Your app password from email


response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

print(iss_latitude)
print(iss_longitude)

#Your position is within +5 or -5 degrees of the ISS position.
def check_position():
    if abs(MY_LAT - iss_latitude) < 5 and abs(MY_LONG - iss_longitude) < 5:
        return True
    else:
        return False


parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

time_now = datetime.now()

print(time_now)
print(sunrise)
print(sunset)

def check_if_dark():
    if time_now.hour < sunrise or time_now.hour > sunset :
        return True
    else:
        return False

while True:
    if check_if_dark() and check_position():
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL, 
                to_addrs=MY_EMAIL, 
                msg=f"Subject:International Space Station\n\nISS now is in your earea, take a look to the sky!"
                )
        time.sleep(300)





