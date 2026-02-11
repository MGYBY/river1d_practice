import cdsapi
import os

def download_era5_t(year1):
    dataset = "derived-era5-single-levels-daily-statistics"
    request = {
        "product_type": ["reanalysis"],
        "variable": ["2m_temperature"],
        "year": [
            year1
        ],
        "month": [
            "01", "02", "03",
            "04", "05", "06",
            "07", "08", "09",
            "10", "11", "12"
        ],
        "day": [
            "01", "02", "03",
            "04", "05", "06",
            "07", "08", "09",
            "10", "11", "12",
            "13", "14", "15",
            "16", "17", "18",
            "19", "20", "21",
            "22", "23", "24",
            "25", "26", "27",
            "28", "29", "30",
            "31"
        ],
        "daily_statistic": "daily_mean",
        "time_zone": "utc+00:00",
        "frequency": "6_hourly",
        "area": [58.5, -111.55, 56.75, -111.2]
    }

    client = cdsapi.Client()
    client.retrieve(dataset, request).download()
    system_command_1 = "mv *.nc"+" "+year1+"_t_reg1.nc"
    system_command_2 = "mv *t_reg1.nc"+" "+"./final_download/"
    os.system(system_command_1)
    os.system(system_command_2)

def download_era5_rad(year1):
    dataset = "derived-era5-single-levels-daily-statistics"
    request = {
        "product_type": ["reanalysis"],
        "variable": ["surface_solar_radiation_downwards"],
        "year": [
            year1
        ],
        "month": [
            "01", "02", "03",
            "04", "05", "06",
            "07", "08", "09",
            "10", "11", "12"
        ],
        "day": [
            "01", "02", "03",
            "04", "05", "06",
            "07", "08", "09",
            "10", "11", "12",
            "13", "14", "15",
            "16", "17", "18",
            "19", "20", "21",
            "22", "23", "24",
            "25", "26", "27",
            "28", "29", "30",
            "31"
        ],
        "daily_statistic": "daily_mean",
        "time_zone": "utc+00:00",
        "frequency": "6_hourly",
        "area": [58.5, -111.55, 56.75, -111.2]
    }

    client = cdsapi.Client()
    client.retrieve(dataset, request).download()
    system_command_1 = "mv *.nc"+" "+year1+"_rad_reg1.nc"
    system_command_2 = "mv *rad_reg1.nc"+" "+"./final_download/"
    os.system(system_command_1)
    os.system(system_command_2)

for year_item in range(2015, 2017):
    download_era5_t(str(year_item))
    download_era5_rad(str(year_item))
