import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests

API_KEY = "a032b4ee760da733f047167cdbbdfc5c"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Weather to image mapping
weather_images = {
    "clear": "clear.png",
    "clouds": "clouds.png",
    "rain": "rain.png",
    "snow": "snow.png",
    "mist": "mist.png",
    "fog": "mist.png"
}

def get_weather_icon(condition):
    return weather_images.get(condition, "default.png")

def get_weather():
    city = entry.get().strip()
    if not city:
        messagebox.showerror("Input Error", "Please enter a city name.")
        return

    url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            condition = data["weather"][0]["main"].lower()
            temp = data["main"]["temp"]
            weather = data["weather"][0]["description"]
            humidity = data["main"]["humidity"]
            wind = data["wind"]["speed"]

            result.set(f"{city}\n{weather.title()}\n{temp}°C\nHumidity: {humidity}%\nWind: {wind} m/s")

            # Update background image
            icon_path = get_weather_icon(condition)
            update_background(icon_path)

        else:
            messagebox.showerror("Error", "City not found or API error.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")

def update_background(image_path):
    img = Image.open(image_path)
    img = img.resize((400, 400))
    photo = ImageTk.PhotoImage(img)
    background_label.config(image=photo)
    background_label.image = photo

# GUI Setup
root = tk.Tk()
root.title("Weather Forecast Dashboard")
root.geometry("400x400")

# Background Image Label
background_label = tk.Label(root)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Entry + Button
entry = tk.Entry(root, font=("Arial", 14))
entry.pack(pady=20)

tk.Button(root, text="Check Weather", command=get_weather, font=("Arial", 12)).pack(pady=10)

result = tk.StringVar()
tk.Label(root, textvariable=result, font=("Arial", 13), bg="white", fg="black").pack(pady=20)

root.mainloop()
