import geopandas
from shapely import geometry
import matplotlib.pyplot as plt

file = "C:/Users/chenyujie/Desktop/Test/yantian.geoJson"
data = geopandas.read_file(file)
print(data)
# cq = geopandas.GeoSeries([geometry.Point([116.0, 39.0])], crs='EPSG:4326')
# fig, ax = plt.subplots()
# data.to_crs(crs='EPSG:4524').plot(ax=ax, color="#4C92C3", alpha=0.8)
# cq.to_crs(crs='EPSG:4524').plot(ax=ax, color='orange', markersize=100, marker='*')
# plt.xticks(rotation=20)
# plt.savefig("C:/Users/chenyujie/Desktop/Test/MapDisplayAndprojection.png")
# plt.show()
