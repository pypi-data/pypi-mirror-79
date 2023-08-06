from scipy import stats
import numpy as np
from microfilter.univariate.runningmoments import RunningKurtosis
from microfilter.univariate.distmachine import DistMachine
from microconventions.stats_conventions import evenly_spaced_percentiles


# Moment based approximate skew normal distribution machine based on this idea:
# https://stackoverflow.com/questions/49801071/how-can-i-use-skewnorm-to-produce-a-distribution-with-the-specified-skew
# A bit of a whim so use at your own risk ! Personally I think it needs some work.


class SkewDist(DistMachine):

    def __init__(self, state:RunningKurtosis=None, num_interp=500, **ignore):
        state = state or RunningKurtosis()
        super().__init__(state=state,params=None)
        self.cached_samples = None
        self.num_interp = num_interp
        self.percentiles = evenly_spaced_percentiles(num=self.num_interp)

    def update(self, value=None, dt=None, **kwargs):
        self.state.update(value=value, dt=dt)
        self.cached_samples = None

    def inv_cdf(self, p):
        if self.cached_samples is None:
            self.cached_samples = sorted(self.skewed_sample(mean=self.state.mean, sd=self.state.std(),
                                                            skew=self.state.skewness(), num=self.num_interp))
        return np.interp(p, self.percentiles, self.cached_samples)

    @staticmethod
    def skewed_sample(mean, sd, skew, num):
        """
              :returns a collection of samples with roughly the supplied mean, standard deviation and skew
        """
        # see https://gist.github.com/microprediction/2f7b5f062c1267d5baab92aefd3bf0f1 for illustration of fit

        # calculate the degrees of freedom 1 required to obtain the specific
        # skewness statistic, derived from simulations
        loglog_slope = -2.211897875506251
        loglog_intercept = 1.002555437670879
        df2 = 500
        df1 = 10 ** (loglog_slope * np.log10(abs(skew)) + loglog_intercept)

        # sample from F distribution
        fsample = np.sort(stats.f(df1, df2).rvs(size=num))

        # adjust the variance by scaling the distance from each point to the
        # distribution mean by a constant, derived from simulations
        k1_slope = 0.5670830069364579
        k1_intercept = -0.09239985798819927
        k2_slope = 0.5823114978219056
        k2_intercept = -0.11748300123471256

        scaling_slope = abs(skew) * k1_slope + k1_intercept
        scaling_intercept = abs(skew) * k2_slope + k2_intercept

        scale_factor = (sd - scaling_intercept) / scaling_slope
        new_dist = (fsample - np.mean(fsample)) * scale_factor + fsample

        # flip the distribution if specified skew is negative
        if skew < 0:
            new_dist = np.mean(new_dist) - new_dist

        # adjust the distribution mean to the specified value
        samples = new_dist + (mean - np.mean(new_dist))
        return samples


