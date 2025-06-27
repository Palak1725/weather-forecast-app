# 🌦️ Weather Forecast App — Python + Tkinter

A clean, functional, and beginner-friendly desktop app that brings **real-time weather updates** straight to your fingertips.

This Python GUI project fetches **live weather data** using the OpenWeatherMap API and offers a **7-day forecast** with detailed meteorological insights — including temperature, pressure, humidity, and wind speed — all rendered in a sleek and minimal interface built with **Tkinter**.

---

## 🔍 Features at a Glance

✅ **Live Weather Data** — Instantly fetches and displays current temperature, humidity, pressure, wind speed, and more.  
✅ **7-Day Forecast** — Scrollable day-wise forecast with weather icons for easy glanceability.  
✅ **City Search** — Just type the city name and hit search — it’s that simple.  
✅ **Auto Geolocation** — Detects your current location using `geopy` and `timezonefinder`.  
✅ **Timezone-Aware** — Displays accurate local time and handles timezones seamlessly.  
✅ **Error Handling** — Graceful API and network error management with user-friendly messages.  
✅ **Minimal UI** — Built with Tkinter for a lightweight yet intuitive interface.  
✅ **Modular Codebase** — Separated logic for API calls, GUI elements, and data parsing for easier understanding and future improvements.

---

## 🛠️ Built With

- **Python 3.x**
- **Tkinter** – GUI library  
- **OpenWeatherMap API** – For real-time weather data  
- **Geopy** – Geolocation via IP  
- **TimezoneFinder** – To fetch accurate local time  
- **Pillow (PIL)** – For handling weather icons

---

## 🤝 Contribution
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## 📜 License
This project is licensed under the MIT License.

## 🙌 Acknowledgements
- OpenWeatherMap for the API

- Geopy for geolocation services

- TimezoneFinder for timezone support

- Pillow for image handling

---

## 🚀 Getting Started

### 🔧 Prerequisites
Make sure Python is installed. Then install required packages using:

```bash
pip install requests geopy timezonefinder pillow
