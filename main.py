from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

stations = pd.read_csv("weather_data/stations.txt", skiprows=17)
stations = stations[["STAID", "STANAME                                 ", "HGHT"]]

@app.route("/")
def home():
    return render_template("home.html", data=stations.to_html())


@app.route("/api/v1/<station>/<date>")  # < > brackets are used in Flask for user-entered values
def about(station, date):
    filename = "weather_data/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    temperature = df.loc[df["    DATE"] == date]["   TG"].squeeze() / 10
    return {"station": station,
            "date": date,
            "temperature": temperature}


@app.route("/api/v1/<station>")
def all_data(station):
    filename = "weather_data/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    #  orient="records" makes a list of dictionaries each representing one row of the DF.
    result = df.to_dict(orient="records")
    return result


@app.route("/api/v1/annual/<station>/<year>")
def year_data(station, year):
    filename = "weather_data/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    df["    DATE"] = df["    DATE"].astype(str)
    result = df[df["    DATE"].str.startswith(str(year))].to_dict(orient="records")
    return result


if __name__ == "__main__":
    app.run(debug=True)
