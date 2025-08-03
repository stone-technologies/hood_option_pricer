import numpy as np
from scipy.stats import norm
from abc import ABC, abstractmethod

class OptionPricer(ABC):
    @abstractmethod
    def call_price(self, S, K, T, r, sigma) -> float: ...
    @abstractmethod
    def put_price(self, S, K, T, r, sigma) -> float: ...

class BlackScholesPricer(OptionPricer):
    def call_price(self, S, K, T, r, sigma):
        if T <= 0:
            return max(S-K, 0.0)
        d1 = (np.log(S/K) + (r+0.5*sigma**2)*T) / (sigma*np.sqrt(T))
        d2 = d1 - sigma*np.sqrt(T)
        return float(S*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2))

    def put_price(self, S, K, T, r, sigma):
        c = self.call_price(S, K, T, r, sigma)
        return float(c - S + K*np.exp(-r*T))

class BinomialCRRPricer(OptionPricer):
    def __init__(self, steps: int):
        self.steps = steps

    def call_price(self, S, K, T, r, sigma):
        if T <= 0:
            return max(S-K, 0.0)
        dt = T/self.steps
        u = np.exp(sigma*np.sqrt(dt))
        d = 1/u
        p = (np.exp(r*dt)-d)/(u-d)
        ST = S * d**np.arange(self.steps,-1,-1) * u**np.arange(0,self.steps+1)
        payoff = np.maximum(ST-K,0.0)
        disc = np.exp(-r*dt)
        for i in range(self.steps,0,-1):
            payoff = disc*(p*payoff[1:i+1] + (1-p)*payoff[:i])
        return float(payoff[0])

    def put_price(self, S, K, T, r, sigma):
        if T <= 0:
            return max(K-S, 0.0)
        dt = T/self.steps; u=np.exp(sigma*np.sqrt(dt)); d=1/u
        p=(np.exp(r*dt)-d)/(u-d)
        ST = S*d**np.arange(self.steps,-1,-1)*u**np.arange(0,self.steps+1)
        payoff=np.maximum(K-ST,0.0); disc=np.exp(-r*dt)
        for i in range(self.steps,0,-1):
            payoff=disc*(p*payoff[1:i+1] + (1-p)*payoff[:i])
        return float(payoff[0])



class MonteCarloPricer(OptionPricer):
    def __init__(self, paths: int):
        self.paths = paths

    def call_price(self, S, K, T, r, sigma):
        if T <= 0:
            return max(S - K, 0.0)
        Z = np.random.standard_normal(self.paths)
        ST = S*np.exp((r-0.5*sigma**2)*T + sigma*np.sqrt(T)*Z)
        return float(np.exp(-r*T)*np.mean(np.maximum(ST-K,0.0)))

    def put_price(self, S, K, T, r, sigma):
        if T <= 0:
            return max(K - S, 0.0)
        Z = np.random.standard_normal(self.paths)
        ST = S*np.exp((r-0.5*sigma**2)*T + sigma*np.sqrt(T)*Z)
        return float(np.exp(-r*T)*np.mean(np.maximum(K-ST,0.0)))
