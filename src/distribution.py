from query import ExternalIdsQuery, ExternalIdCountQuery
import matplotlib.pyplot as plt
import operator
import pandas as pd


class ExternalIdDistribution(object):

    def __init__(self, size=50):
        self.size = size
        self.distribution = None

    def calculate(self):

        distribution = {}
        external_ids = ExternalIdsQuery().execute().extract()
        print(external_ids)

        for external_id in external_ids:

            count = ExternalIdCountQuery(external_id['property']).execute().extract()

            if len(distribution.keys()) >= self.size:
                if min(distribution.values()) < count:
                    distribution.pop(min(distribution, key=distribution.get))
                    distribution[external_id['propertyLabel']] = count
            else:
                distribution[external_id['propertyLabel']] = count

        self.distribution = distribution

        return self

    def plot(self):
        distribution = list(zip(*sorted(self.distribution.items(), key=operator.itemgetter(1))))
        series = pd.Series(data=distribution[1][::-1], index=distribution[0][::-1])
        series.plot.bar()
        plt.savefig('../plots/distribution.pdf')

