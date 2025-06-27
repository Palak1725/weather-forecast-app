from tkinter import *
import tkinter as tk
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import *
import requests
import pytz
from PIL import Image, ImageTk

root = Tk()
root.title("Weather Forecasting App")
root.geometry("890x470+300+300")
root.config(bg = "#93c9f5")
root.resizable(False, False)

def getWeather():
    city = textfield.get()
    geolocator = Nominatim(user_agent="weather_forecast_app_by_palak")
    try:
        location = geolocator.geocode(city)
        if location:
            obj = TimezoneFinder()
            result = obj.timezone_at(lng=location.longitude, lat=location.latitude)
            timezone.config(text=result)
            lat = location.latitude
            lon = location.longitude
            lat_direction = "N" if lat >= 0 else "S"
            lon_direction = "E" if lon >= 0 else "W"
            formatted_lat = f"{abs(round(lat, 4))}°{lat_direction}"
            formatted_lon = f"{abs(round(lon, 4))}°{lon_direction}"
            long_lat.config(text=f"{formatted_lat}, {formatted_lon}")

            home = pytz.timezone(result)
            local_time = datetime.now(home)
            current_time = local_time.strftime("%I:%M %p")
            clock.config(text=current_time)

            #weather
            api = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid=f514bf0538f952cf9136ad5f9950d674"
            response = requests.get(api)
            json_data = response.json()

            if response.status_code != 200:
                timezone.config(text="API Error")
                long_lat.config(text=json_data.get("message", "Unknown Error"))
                return

            #current
            temp = json_data['main']['temp']
            humidity = json_data['main']['humidity']
            pressure = json_data['main']['pressure']
            wind = json_data['wind']['speed']
            description = json_data['weather'][0]['description']

            t.config(text=f"{temp}°C")
            h.config(text=f"{humidity}%")
            p.config(text=f"{pressure} hPa")
            w.config(text=f"{wind} m/s")
            d.config(text=description.strip())

            from io import BytesIO
            from collections import OrderedDict

            forecast_api = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=metric&appid=f514bf0538f952cf9136ad5f9950d674"
            forecast_response = requests.get(forecast_api)
            forecast_data = forecast_response.json()

            if forecast_response.status_code != 200:
                print("Forecast API Error:", forecast_data.get("message", "Unknown error"))
                return

            forecast_list = forecast_data['list']
            today = datetime.now().date()

            from collections import defaultdict
            grouped = defaultdict(list)

            for entry in forecast_list:
                dt = datetime.strptime(entry['dt_txt'], "%Y-%m-%d %H:%M:%S")
                grouped[dt.date()].append(entry)

            final_forecast = OrderedDict()
            count = 0
            grouped = dict(sorted(grouped.items()))  # sort dates

            for date_key, entries in grouped.items():
                if count == 7:
                    break
                icon = entries[0]['weather'][0]['icon']
                min_temp = min(e['main']['temp_min'] for e in entries)
                max_temp = max(e['main']['temp_max'] for e in entries)
                label = "Today" if date_key == today else "Tomorrow" if date_key == today + timedelta(days=1) else datetime.strftime(date_key, "%a")
                full_label = f"{date_key.strftime('%m/%d')} {label}"
                final_forecast[date_key] = {
                    "label": full_label,
                    "icon": icon,
                    "min": round(min_temp),
                    "max": round(max_temp),
                }
                count += 1

            # Update display
            day_labels = [day1, day2, day3, day4, day5, day6, day7]
            icons = [firstimage, secondimage, thirdimage, fourthimage, fifthimage, sixthimage, seventhimage]

            final_forecast_list = list(final_forecast.items())[:7]  # Only take first 7 valid items

            print("Forecast Count:", len(final_forecast))  # debug

            for i in range(7):
                if i < len(final_forecast_list):
                    date, data = final_forecast_list[i]
                    day_labels[i].config(text=data["label"])

                    icon_url = f"http://openweathermap.org/img/wn/{data['icon']}@2x.png"
                    icon_response = requests.get(icon_url)
                    img = Image.open(BytesIO(icon_response.content)).resize((50, 50))
                    icon_img = ImageTk.PhotoImage(img)
                    icons[i].config(image=icon_img)
                    icons[i].image = icon_img  # hold reference

                    temp_labels[i].config(text=f"{data['min']}°/{data['max']}°")
                else:
                    day_labels[i].config(text="")
                    icons[i].config(image="")
                    icons[i].image = None
                    temp_labels[i].config(text="")



        else:
            timezone.config(text="City Not Found")
            long_lat.config(text="")
            clock.config(text="")

    except Exception as e:
        timezone.config(text="Error")
        long_lat.config(text="")
        clock.config(text="")
        print("Error:", e)

#icon
image_icon = PhotoImage(file = r"C:\Users\palak\.vscode\Weather Forecast App\Images\logo.png")
root.iconphoto(False, image_icon)

#search box
search_image = PhotoImage(file = r"C:\Users\palak\.vscode\Weather Forecast App\Images\Rounded Rectangle 3.png")
myimage = Label(root, image = search_image, bg = "#93c9f5")
myimage.place(x = 290, y = 120)

weat_image = PhotoImage(file = r"C:\Users\palak\.vscode\Weather Forecast App\Images\Layer 7.png")
weatherimage = Label(root, image = weat_image, bg = "#203243")
weatherimage.place(x = 310, y = 127)

textfield = tk.Entry(root, justify = 'center', width = 15, font = ("poppins", 25, 'bold'), bg = "#203243", border = 0, fg = "white")
textfield.place(x = 390, y = 130)
textfield.focus()

search_icon = PhotoImage(file = r"C:\Users\palak\.vscode\Weather Forecast App\Images\Layer 6.png")
myimage_icon = Button(root, image = search_icon, borderwidth = 0, cursor = "hand2", bg = "#203243", command = getWeather)
myimage_icon.place(x = 665, y = 125)

#Bottom Box
frame = Frame(root, width = 900, height = 180, bg = "#212120")
frame.pack(side = BOTTOM)

#Bottom Boxes
firstbox = PhotoImage(file = r"C:\Users\palak\.vscode\Weather Forecast App\Images\Rounded Rectangle 2.png")
secondbox = PhotoImage(file = r"Weather Forecast App/Images/Rounded Rectangle 2 copy.png")

Label(frame, image = firstbox, bg = "#212120").place(x = 30, y = 20)
Label(frame, image = secondbox, bg = "#212120").place(x = 300, y = 30)
Label(frame, image = secondbox, bg = "#212120").place(x = 400, y = 30)
Label(frame, image = secondbox, bg = "#212120").place(x = 500, y = 30)
Label(frame, image = secondbox, bg = "#212120").place(x = 600, y = 30)
Label(frame, image = secondbox, bg = "#212120").place(x = 700, y = 30)
Label(frame, image = secondbox, bg = "#212120").place(x = 800, y = 30)

#clock
clock = Label(root, font = ("Helvetica", 30, 'bold'), fg = "white", bg = "#93c9f5")
clock.place(x = 30, y = 20)

#timezone
timezone = Label(root, font = ("Helvetica", 20, 'bold'), fg = "white", bg = "#93c9f5")
timezone.place(x = 690, y = 20)

long_lat = Label(root, font = ("Helvetica", 10), fg = "white", bg = "#93c9f5")
long_lat.place(x = 690, y = 50)

#thpwd
# Weather Info Frame
weather_frame = Frame(root, bg="#203243", bd=2, relief="ridge", width=250, height=135)
weather_frame.place(x=20, y=80)
weather_frame.pack_propagate(False)

#labels and values
Label(weather_frame, text="Temperature", font=("Helvetica", 11, "bold"), fg="white", bg="#203243").grid(row=0, column=0, sticky="w", padx=10, pady=2)
Label(weather_frame, text="Humidity", font=("Helvetica", 11, "bold"), fg="white", bg="#203243").grid(row=1, column=0, sticky="w", padx=10, pady=2)
Label(weather_frame, text="Pressure", font=("Helvetica", 11, "bold"), fg="white", bg="#203243").grid(row=2, column=0, sticky="w", padx=10, pady=2)
Label(weather_frame, text="Wind Speed", font=("Helvetica", 11, "bold"), fg="white", bg="#203243").grid(row=3, column=0, sticky="w", padx=10, pady=2)
Label(weather_frame, text="Description", font=("Helvetica", 11, "bold"), fg="white", bg="#203243").grid(row=4, column=0, sticky="nw", padx=10, pady=2)

t = Label(weather_frame, font=("Helvetica", 11), fg="white", bg="#203243")
t.grid(row=0, column=1, sticky="w", padx=10)
h = Label(weather_frame, font=("Helvetica", 11), fg="white", bg="#203243")
h.grid(row=1, column=1, sticky="w", padx=10)
p = Label(weather_frame, font=("Helvetica", 11), fg="white", bg="#203243")
p.grid(row=2, column=1, sticky="w", padx=10)
w = Label(weather_frame, font=("Helvetica", 11), fg="white", bg="#203243")
w.grid(row=3, column=1, sticky="w", padx=10)
d = Message(weather_frame, font=("Helvetica", 11), fg="white", bg="#203243", width=200)
d.grid(row=4, column=1, sticky="w", padx=10)

#first box labels
firstframe = Frame(root, width = 230, height = 132, bg = "#282829")
firstframe.place(x = 35, y = 315)

day1 = Label(firstframe, font = "arial 20", fg = "#fff", bg = "#282829")
day1.place(relx = 0.5, anchor = "n", y = 5)

firstimage = Label(firstframe, bg = "#282829")
firstimage.place(relx = 0.5, anchor = "n", y = 35)

#second box labels
secondframe = Frame(root, width = 70, height = 115, bg = "#282829")
secondframe.place(x = 305, y = 325)

day2 = Label(secondframe, fg = "#fff", bg = "#282829")
day2.place(relx = 0.5, anchor = "n", y = 5)

secondimage = Label(secondframe, bg = "#282829")
secondimage.place(x = 7, y = 20)

#third box labels
thirdframe = Frame(root, width = 70, height = 115, bg = "#282829")
thirdframe.place(x = 405, y = 325)

day3 = Label(thirdframe, fg = "#fff", bg = "#282829")
day3.place(relx = 0.5, anchor = "n", y = 5)

thirdimage = Label(thirdframe, bg = "#282829")
thirdimage.place(x = 7, y = 20)

#fourth box labels
fourthframe = Frame(root, width = 70, height = 115, bg = "#282829")
fourthframe.place(x = 505, y = 325)

day4 = Label(fourthframe, fg = "#fff", bg = "#282829")
day4.place(relx = 0.5, anchor = "n", y = 5)

fourthimage = Label(fourthframe, bg = "#282829")
fourthimage.place(x = 7, y = 20)

#fifth box labels
fifthframe = Frame(root, width = 70, height = 115, bg = "#282829")
fifthframe.place(x = 605, y = 325)

day5 = Label(fifthframe, fg = "#fff", bg = "#282829")
day5.place(relx = 0.5, anchor = "n", y = 5)

fifthimage = Label(fifthframe, bg = "#282829")
fifthimage.place(x = 7, y = 20)

#sixth box labels
sixthframe = Frame(root, width = 70, height = 115, bg = "#282829")
sixthframe.place(x = 705, y = 325)

day6 = Label(sixthframe, fg = "#fff", bg = "#282829")
day6.place(relx = 0.5, anchor = "n", y = 5)

sixthimage = Label(sixthframe, bg = "#282829")
sixthimage.place(x = 7, y = 20)

#seventh box labels
seventhframe = Frame(root, width = 70, height = 115, bg = "#282829")
seventhframe.place(x = 805, y = 325)

day7 = Label(seventhframe, fg = "#fff", bg = "#282829")
day7.place(relx = 0.5, anchor = "n", y = 5)

seventhimage = Label(seventhframe, bg = "#282829")
seventhimage.place(x = 7, y = 20)

temp_frames = [firstframe, secondframe, thirdframe, fourthframe, fifthframe, sixthframe, seventhframe]
temp_labels = []

for frame in temp_frames:
    lbl = Label(frame, bg="#282829", fg="#57adff", font="arial 10 bold")
    lbl.place(relx=0.5, anchor="n", y=85)
    temp_labels.append(lbl)


root.mainloop()