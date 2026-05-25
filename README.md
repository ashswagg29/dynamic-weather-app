# 🌤️ Dynamic Weather Application

A modern, responsive, and visually dynamic desktop weather application built with Python and Tkinter. 
The application fetches real-time weather data and 5-day forecasts using the OpenWeatherMap API, 
while featuring a custom physics-based particle system that adapts to current atmospheric conditions.

---

## 🛠️ SYSTEM REQUIREMENTS, DEPENDENCIES & HOW TO RUN

### 1. System Requirements
* Python 3.x installed on your local machine.
* Standard built-in libraries used: `tkinter`, `math`, `random`, `datetime`, `io` (No installation needed for these).

### 2. External Dependencies (Third-Party Libraries)
You must install the following external libraries before running the application:
* **requests**: To fetch real-time JSON payloads from OpenWeatherMap API.
* **pillow (PIL)**: For dynamic image generation and rendering background gradients.

To install both requirements at once, run this command in your terminal:
```bash
pip install requests pillow

✨ Features
Real-Time Data: Live weather statistics including temperature, perceived temperature, wind speed, and humidity.

5-Day / 3-Hour Forecast: Detailed atmospheric projections displayed in an organized, alternating-color data grid.

Dynamic Theme & Particle Engine: The interface morphs visually based on the target city's weather, generating localized canvas effects
(Sunny, Cloudy, Rainy, Snowy, Foggy, Stormy).

Fully Responsive Geometry: UI layout automatically scales, repositions components,
and scales typography dynamically upon window resizing or entering F11 Fullscreen Mode.

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

