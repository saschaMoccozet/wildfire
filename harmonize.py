import numpy as np
import rasterio
import matplotlib.pyplot as plt
import xarray as xr
import rioxarray as rxr
import geopandas as gpd






# Definition of a function to check on the dataset open before combining them
def print_raster(raster):
    """Prints the raster's metadata and shape"""
    print(
        f"shape: {raster.rio.shape}\n"
        f"resolution: {raster.rio.resolution()}\n"
        f"bounds: {raster.rio.bounds()}\n"
        f"sum: {raster.sum().item()}\n"
        f"CRS: {raster.rio.crs}\n"
    )


# Open the data
def open_data(path):
    """Opens the data"""
    "input: path to the data"
    return rxr.open_rasterio(path, masked=True).squeeze()


# Resample the data to daily values
# Definition of a function to resample the data to daily values
def resample_to_daily(dataray):
    """Resamples the dataray to daily values"""
    return dataray.resample(time="1D").interpolate("linear")

# definition of a common grid to interpolate from a dataset to another
common_grid = rxr.open_rasterio("datasets/ndvi_01012010_09012022.nc").isel(time=0)

# Definition of a function to interpolate the data to a common grid
def interpolate_to_common_grid(dataray):
    """Interpolates the dataray to a common grid"""
    return dataray.rio.reproject_match(common_grid)


# Definition of the area of interest
# Definition of a function to define the area of interest
def define_area_of_interest(aoi):
    """Defines the area of interest"""
    "input: path to aoi's shapefile"
    crop_extent = gpd.read_file(aoi)
    return crop_extent


# print the crs of the data
# Definition of a function to print the crs of the data
def print_crs(dataray):
    """Prints the crs of the dataray"""
    return print(dataray.rio.crs)


# Definition of a function to print the crs of the crop_extent
def print_crs_crop_extent(crop_extent):
    """Prints the crs of the crop_extent"""
    return print(crop_extent.crs)


# defining a crs for the dataray
# Definition of a function to define a crs for the dataray
def define_crs(dataray, crs=2154):
    """Defines a crs for the dataray"""
    return dataray.rio.write_crs(crs, inplace=True)


# Reproject a dataray from longlat to Lambert93
# Definition of a function to reproject a dataray from longlat to Lambert93
def reproject_to_lambert93(dataray):
    """Reprojects a dataray from longlat to Lambert93"""
    return dataray.rio.reproject("EPSG:2154")


# Reproject a dataray from Lambert93 to longlat
# Definition of a function to reproject a dataray from Lambert93 to longlat
def reproject_to_longlat(dataray):
    """Reprojects a dataray from Lambert93 to longlat"""
    return dataray.rio.reproject("EPSG:4326")


# clip the data to another dataray
# Definition of a function to clip the data to another dataray
def clip_to(dataray, dataray_to_clip_to):
    """Clips the dataray to another dataray"""
    return dataray.rio.clip(dataray_to_clip_to.rio.bounds(), dataray_to_clip_to.rio.crs)


# Clip the data to a shapefile
# Definition of a function to clip the data to a shapefile
def clip_to_shapefile(dataray, path):
    """Clips the dataray to a shapefile"""
    "input: dataray, path to the shapefile"
    return dataray.rio.clip(path)


# Clip the geotiff file to the netcdf file
# Definition of a function to clip the geotiff file to the netcdf file
def clip_geotiff_to_netcdf(geotiff, netcdf):
    """Clips the geotiff file to the netcdf file"""
    "input: geotiff, netcdf"
    return clip_to(geotiff, netcdf)


# Clip the geotiff file with a shapefile
# Definition of a function to clip the geotiff file with a shapefile
def clip_geotiff_with_shapefile(geotiff, path):
    """Clips the geotiff file with a shapefile"""
    "input: geotiff, path to the shapefile"
    return clip_to_shapefile(geotiff, path)


# Merge a geotiff file with a netcdf file
# Definition of a function to merge a geotiff file with a netcdf file
def merge_geotiff_netcdf(geotiff, netcdf):
    """Merges a geotiff file with a netcdf file"""
    "input: geotiff, netcdf"
    return xr.merge([geotiff, netcdf])


# Definition of a function to harmonize the data to a common grid
def harmonize(dataray):
    """Harmonizes the dataray to a common grid"""
    return interpolate_to_common_grid(resample_to_daily(dataray))


# Definition of a function to merge multiple datasets
def merge_multiple(datarays):
    """Merges multiple datarays"""
    return xr.merge(datarays)


# Harmonize a list of datasets
# Definition of a function to harmonize a list of datarays
def harmonize_multiple(datarays):
    """Harmonizes a list of datarays
    into a single harmonized dataray"""
    """
    input: list of datarays
    output: harmonized dataray
    """
    return merge_multiple([harmonize(dataray) for dataray in datarays])


# Export the harmonized data into a netcdf file
# Definition of a function to export the harmonized data into a netcdf file
def export_to_netcdf(dataray, path):
    """Exports the dataray into a netcdf file"""
    "input: dataray, path to the netcdf file"
    return dataray.to_netcdf(path)


# Read the data exported from the harmonize.py script
# Definition of a function to read the data exported from the harmonize.py script
def read_data(path):
    """Reads the data exported from the harmonize.py script"""
    "input: path to the data"
    return xr.open_dataset(path)

#plot the one variable
# Definition of a function to plot the one variable at a specific time
def plot_one_variable(dataray, variable, time):
    """Plots the one variable at a specific time"""
    "input: dataray, variable, time"
    return dataray[variable].sel(time=time).plot()

# Multiple plots of one variable over time range
# Definition of a function to plot multiple plots of one variable over time range
def plot_multiple(dataray, variable, time_range):
    """Plots multiple plots of one variable over time range"""
    "input: dataray, variable, time_range"
    return dataray[variable].sel(time=time_range).plot(col="time", col_wrap=4)



if __name__ == "__main__":
    # Open the data
    # definition of a common grid to interpolate from a dataset to another
    common_grid = rxr.open_rasterio("datasets/ndvi_01012010_09012022.nc").isel(time=0)
    # definition of the area of interest
    crop_extent = define_area_of_interest("mygeodata.zip")
    # open the data
    ndvi = read_data("datasets/ndvi_01012010_09012022.nc")
    # open the data
    evapotranspiration = read_data("datasets/Evapotranspiration_500m_aid0001.nc")
    # open the data
    era = read_data(
        "datasets/adaptor.mars.internal-1663249407.7272627-22718-12-e830357e-7728-41cf-9b2b-b7f34cabf652.nc")
    # open the data
    burn_date = read_data("datasets/burn_date_01012010_09012022.nc")
    # open the data
    burn_mask = read_data("datasets/fire_mask_01012010_09012022.nc")
    # open the data
    density = read_data("datasets/fra_pd_2015_1km_UNadj.tif")
    # open the data
    leaf_area_index = read_data("datasets/leaf_area_index_01012010_09012022.nc")
    # open the data
    lst_day = read_data("datasets/LST_1km_01012010_09012022 (1).nc")
    # open the data
    lst_night = read_data("datasets/LST_Night_1km_01012010_09012022.nc")
    # open the data
    lst_qc = read_data("datasets/MOD11A1.061_1km_aid0001.nc")


    # Clip the density data to the area of interest
    density = clip_geotiff_with_shapefile(density, "mygeodata.zip")
    #Clip the era data to the area of interest
    era = clip_to_shapefile(era, "mygeodata.zip")

    # Reproject era data from longlat to Lambert93
    era = reproject_to_lambert93(era)
    # Reproject density data from longlat to Lambert93
    density = reproject_to_lambert93(density)


    # create a list of the data
    data = [
        ndvi,
        evapotranspiration,
        era,
        burn_date,
        burn_mask,
        density,
        leaf_area_index,
        lst_day,
        lst_night,
        lst_qc,
    ]
    #

    # Defining the crs of the data
    crs = "EPSG:2154"
    # Defining the bounds of the data
    bounds = crop_extent.bounds
    # Defining the resolution of the data
    resolution = (1000, 1000)
    # Defining the name of the data
    name = "harmonized_data"
    # Defining the path to the data
    outfile = "datasets/harmonized_data.nc"

    # Harmonize the data
    harmonized_data = harmonize_multiple(data)
    # Export the harmonized data into a netcdf file
    export_to_netcdf(harmonized_data, "outfile")
    # Read the data exported from the harmonize.py script
    harmonized_data = read_data("outfile")
    # Plot the one variable at a specific time
    plot_one_variable(harmonized_data, "dvi", "2010-01-01")
    # Plot multiple plots of one variable over time range
    plot_multiple(harmonized_data, "dvi", slice("2010-01-01", "2010-01-31"))

