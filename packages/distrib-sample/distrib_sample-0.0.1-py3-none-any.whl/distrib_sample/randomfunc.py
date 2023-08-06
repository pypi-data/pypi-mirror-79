from scipy.stats import norm,poisson,binom


def randomdraw(length,distrib, **kwargs):
    '''
    
    Parameters
    ----------
    length : number of samples
    distrib : distribution - 0 for normal,
                             1 for binomial or 
                             2 for poisson
    **kwargs : distribution parameters
               for normal loc keyword specifies mean, scale keyword specifies sd
               for binomial n and p specify shape parameters,loc keyword shifts distribution
               for poisson  mu specifies shape parameter,loc keyword shifts distribution
    Returns
    -------
    A sample of random numbers of the specified length from the specified distribution

    '''
    if distrib == 0:
        return norm(**kwargs).rvs(size=length)
    elif distrib == 1:
        return binom(**kwargs).rvs(size=length)
    elif distrib == 2:
        return poisson(**kwargs).rvs(size=length)
    else:
        print('Invalid choice of distrib')
    
  
'''
Examples  
randomdraw(10,0)
randomdraw(2,2,mu=0.1)
randomdraw(5,1,n=3,p=0.5)
randomdraw(10,5)
'''