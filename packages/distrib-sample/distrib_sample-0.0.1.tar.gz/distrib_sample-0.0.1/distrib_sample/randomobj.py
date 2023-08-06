from scipy.stats import norm,binom,poisson

class Distrib:

    def __init__(self,length,distrib, **kwargs):
        '''
        Attributes
        ----------
        length : The length of the random sample
        distrib : distribution - 0 for normal,
                                 1 for binomial or 
                                 2 for poisson
        **kwargs : distribution parameters
               for normal loc keyword specifies mean, scale keyword specifies sd
               for binomial n and p specify shape parameters,loc shifts distribution
               for poisson  mu specifies shape parameter,loc shifts distribution
        
        '''

        self.length = length
        if distrib == 0:
            self.distrib = norm(**kwargs)
        elif  distrib ==1:
            self.distrib =binom(**kwargs)
        elif distrib ==2:
            self.distrib = poisson(**kwargs)
        self.__dict__.update(**kwargs)
    
    
    def draw(self):
        '''
        Method to draw sample of specified length from the distribution

        Returns
        -------
        sample of random numbers of the specified length from the specified distribution

        '''
        self.draw = self.distrib.rvs(size=self.length)
        return self.draw
    
    
    def summarise(self):
        '''
        Method to print stats of a drawn sample

        Returns
        -------
        None.

        ''' 
        print("Min of the Sample is %s"%self.draw.min())
        print("Max of the Sample is %s"%self.draw.max())
        print("Mean of the Sample is %s"%self.draw.mean())
        print("SD of the Sample is %s"%self.draw.std())

'''
Examples
normaldist = Distrib(10,0,loc=5)
normaldist.loc
normaldist.draw()
normaldist.summarise()

poissondist=Distrib(10,2,mu=0.7)
poissondist.draw()
poissondist.summarise()

binomdist = Distrib(5,1,n=6,p=1)
binomdist.draw()
binomdist.summarise()
'''


