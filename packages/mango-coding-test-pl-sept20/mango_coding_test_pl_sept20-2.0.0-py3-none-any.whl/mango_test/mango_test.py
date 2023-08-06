import numpy as np

def random_draw(nsamples, dist, **params):
    
    """
    nsamples: number of samples to return (integer; >= 0)
    dist: chosen distribution (string; 'normal', 'poisson', or 'binomial')
    params: keyword arguments for parameterising distribution
    
        dist = 'normal'; params mean and sd (standard deviation)
        dist = 'poisson'; params n and p
        dist = 'binomial'; params lam (lambda)
        
    """
    
    if dist == 'normal':
        
        mean = params['mean']
        sd = params['sd']
        
        return sd * np.random.randn(nsamples) + mean
    
    elif dist == 'poisson':
        
        lam = params['lam']
        
        return np.random.poisson(lam, size=nsamples)
    
    elif dist == 'binomial':
        
        n = params['n']
        p = params['p']
        
        return np.random.binomial(n, p, size=nsamples)
    
    else:
        print('dist must be normal, poisson or binomial')
        return

class Sample:
    
    sample = np.array([])
    
    def __init__(self, dist):

        if dist not in ['normal', 'binomial', 'poisson']:
            raise Exception('dist must be normal, poisson or binomial')
        self.dist = dist
    
    def draw(self, nsamples):
        
        """
        Updates self.sample with numpy array of length nsamples,
        comprising of randomly drawn samples from self.dist distribution.
        """
                
        if self.dist == 'normal':
            mean = self.mean
            sd = self.sd
            self.sample = sd * np.random.randn(nsamples) + mean
    
        elif self.dist == 'poisson':
            lam = self.lam
            self.sample = np.random.poisson(lam, size=nsamples)
    
        elif self.dist == 'binomial':
            n = self.n
            p = self.p
            self.sample = np.random.binomial(n, p, size=nsamples)
    
        else:
            print('dist must be normal, poisson or binomial')
    
    def summarise(self):
        
        if self.sample.size > 0:
        
            print('Min:                ', self.sample.min())
            print('Max:                ', self.sample.max())
            print('Mean:               ', self.sample.mean())
            print('Standard Deviation: ', self.sample.std())
            
        else:
            
            print('Non-zero sized sample must be drawn first')
