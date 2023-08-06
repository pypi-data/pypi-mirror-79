import pandas as pd

import cea.config
import cea.inputlocator
from cea.constants import HOURS_IN_YEAR
from cea.utilities import dbf

__author__ = "Jimeno A. Fonseca"
__copyright__ = "Copyright 2017, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Jimeno A. Fonseca", "Sreepathi Bhargava Krishna"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "cea@arch.ethz.ch"
__status__ = "Production"


def calc_spatio_temporal_visuals(locator, period, variables_to_plot, list_of_buildings, initial_date):
    # now the dates in which the building demand is calculated is stored in 'date'
    date = pd.date_range(initial_date, periods=HOURS_IN_YEAR, freq='H')[period[0]: period[1]]
    time = date.strftime("%Y%m%d%H%M%S")

    # this loop checks if all the buildings are selected and gets the building names from Total demand.csv file
    if 'all' in list_of_buildings:
        building_names = pd.read_csv(locator.get_total_demand())['Name'].values
    else:
        building_names = list_of_buildings

    for i, building in enumerate(building_names):
        # importing corresponding variables of each building and then slicing it to take just a single period value
        # i.e a time step
        data = pd.read_csv(locator.PVT_results(building))[variables_to_plot][period[0]: period[1]]
        data['date'] = time
        data['Name'] = building
        data['rad_kWh/m2'] = data['radiation_kWh'] / data['Area_PVT_m2']

        if i == 0:
            final = data
        else:
            final = final.append(data, ignore_index=True)

    dbf.dataframe_to_dbf(final, locator.get_4D_pvt_plot(period))


def main(config):
    locator = cea.inputlocator.InputLocator(scenario=config.scenario)

    variables_to_plot = ['E_PVT_gen_kWh', 'radiation_kWh', 'Q_PVT_gen_kWh', 'Area_PVT_m2']
    initial_date = '1/1/2015'
    list_of_buildings = ['all']  # 'all' for all buildings or else provide a list of building names
    period = [1680, 1848]  # period in hours of the year to viualize
    calc_spatio_temporal_visuals(locator, period, variables_to_plot, list_of_buildings, initial_date)


if __name__ == '__main__':
    main(cea.config.Configuration())
