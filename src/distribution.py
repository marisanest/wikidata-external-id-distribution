import matplotlib.pyplot as plt
import pandas as pd
import os

from query import ExternalIdsQuery, ExternalIdCountQuery
from exceptions import TypeError


class ExternalIdDistribution(object):

    def __init__(self, size=50, plot_save_path='../plots/distribution.pdf', csv_save_path='../csv/distribution.csv'):
        self.size = size
        self.plot_save_path = plot_save_path
        self.csv_save_path = csv_save_path

        if not os.path.exists(os.path.dirname(self.plot_save_path)):
            os.makedirs(os.path.dirname(self.plot_save_path))

        if not os.path.exists(os.path.dirname(self.csv_save_path)):
            os.makedirs(os.path.dirname(self.csv_save_path))

        self.distribution = None

    def calculate(self):

        distribution = {}
        external_ids = ExternalIdsQuery().execute().extract()

        for external_id in external_ids:

            try:
                count = ExternalIdCountQuery(external_id['property']).execute().extract()
            except:
                print('WARNING: External-Identifier ' + external_id['property'] + ' could not be queried and will not '
                                                                                  'be included into the calculation.')
                continue

            if len(distribution.keys()) >= self.size:
                if min(distribution.values()) < count:
                    distribution.pop(min(distribution, key=distribution.get))
                    distribution[external_id['propertyLabel']] = count
            else:
                distribution[external_id['propertyLabel']] = count

        self.distribution = pd.DataFrame(list(distribution.values()), distribution.keys(), ['Count']).sort_values(['Count'], ascending=[False])

        return self

    def plot(self):
        ax = self.distribution[['Count']].plot(kind='bar', title="External-Id Distribution", figsize=(15, 10), legend=True, fontsize=8)
        ax.set_xlabel("External-Id", fontsize=12)
        ax.set_ylabel("Count", fontsize=12)
        plt.savefig(self.plot_save_path)

        return self

    def save(self):
        if self.distribution is None:
            raise TypeError('distribution')
        if not isinstance(self.distribution, pd.DataFrame):
            raise TypeError('distribution', allow=[pd.DataFrame])

        self.distribution.to_csv(self.csv_save_path)

        return self
