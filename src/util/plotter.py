import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from dateutil import parser
from datetime import datetime, timedelta

from util.config import FIGURE_FILE


class Plotter:
    def __init__(self):
        pass

    def _list_dates(self, start_date):
        dates = []
        today = datetime.now()
        delta = timedelta(days=1)
        start_date = parser.parse(start_date)
        while start_date < today:
            dates.append(start_date.strftime('%d.%m.'))
            start_date += delta
        return dates

    def _get_averages(self, scores):
        return [score['average'] for score in scores]

    def _parse_to_pd(self, scores):
        return pd.Series([i if i else np.nan for i in scores])

    def _fill_nones(self, scores):
        n = len(scores)
        for i in range(1, n):
            prev = scores[i-1]
            if scores[i] == np.nan:
                scores[i] = prev
        return scores

    def _parse_to_valid_plot_input(self, scores):
        scores = self._get_averages(scores)
        scores = self._parse_to_pd(scores)
        scores = self._fill_nones(scores)
        return scores

    def _get_name(self, scores):
        return scores[0]['name']

    def clear(self):
        plt.clf()

    def plot(self, scores, start_date, name):
        dates = self._list_dates(start_date)
        y = self._parse_to_valid_plot_input(scores)
        plt.plot(dates, y, label=name, marker='o')

    def save(self):
        plt.legend()
        plt.savefig(FIGURE_FILE, dpi=800)
        self.clear()

    def show(self):
        plt.show()
