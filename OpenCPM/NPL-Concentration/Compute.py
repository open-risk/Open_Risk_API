# encoding: utf-8

# (c) 2018 Open Risk, all rights reserved
#
# Concentration Library is licensed under the MIT license a copy of which is included
# in the source distribution of TransitionMatrix. This is notwithstanding any licenses of
# third-party software included in this distribution. You may not use this file except in
# compliance with the License.
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions and
# limitations under the License.


"""
Created on Fri Nov 18 14:24:07 CET 2017
@author: Open Risk
Purpose: Implement flask based Open Risk API Model Server
Version: 0.2

Compute.py orchestrates model calculations
- may invoke further libraries
- dependencies are numpy / pandas
- handles python data formats

"""

import pandas as pd
from pandas.io.json import json_normalize
import concentration_library as cl


def calculate(model_name, calculation_input):

    # Input is in the form of two json arrays
    # x -> dimension (id, geography, sector etc)
    # y -> exposure

    # Step 1: Aggregate data by dimension

    data = pd.DataFrame()
    data['x'] = calculation_input['x']
    data['y'] = calculation_input['y']

    # Group by x dimension
    portfolio_data = data.groupby(data['x']).sum()

    # Step 2: Perform index calculation
    if model_name in {'Gini_Index', 'HHI_Index', 'Shannon_Index'}:

        # Perform the calculation
        # (invokes the concentration library module)
        result = calculate_index(model_name, portfolio_data['y'])

    else:
        result = "No Suitable Model"

    return result


# the concentration index collection (ADD OTHER functions)
def calculate_index(model_name, exposures):

    # Step 1: Calculate positions weights
    weights = cl.get_weights(exposures)

    # Step 2: Calculate index
    if model_name == 'Shannon_Index':
        value = cl.shannon(weights)
    elif model_name == 'HHI_Index':
        value = cl.hhi(weights)
    elif model_name == 'Gini_Index':
        value = cl.gini(weights)

    return {model_name: value}
