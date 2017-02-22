def skier_generator_process(env, arrivals):
    """ Implementation of the process that generates arriving customers to the facility.
    
        Arguments
        env       --  simpy simulation environment object
        arrivals  --  a list to hold the time of arrivals
    """
   
    k = 0 # A counter to indicate the number of skiers created
    while True:
        # Endless loop
        yield env.timeout( random.expovariate(arrival_freq(env.now)) ) # Wait for a random interval, depending on time of day
        k += 1
        #print( "Time is %6.2f and skier %d arrives" % (env.now, k) )
        arrivals.append(env.now) # Register the time of arrival
        
env = simpy.Environment() # Create the simulation environment
lmbda = 0.5 # One arrival per two minutes on average
arr = [] # The list of arrival times
env.process( skier_generator_process(env, arr) ) # Tell the simulator to process the skier generator process
env.run(until=60*8) # Simulate a day


interArrivalTimesAM = np.diff( np.array( [t for t in arr if t<(12-8)*60] ) ) # The interarrival times first half of the day
interArrivalTimesPM = np.diff( np.array( [t for t in arr if t>(12-8)*60] ) ) # The interarrival times second half of the day

plt.figure(figsize=(16,6))
plt.subplot(121)
plt.hist(interArrivalTimesAM)
plt.title('Interarrival times before noon')
plt.xlim( (0, 15))
plt.subplot(122)
plt.hist(interArrivalTimesPM)
plt.title('Interarrival times afternoon')
plt.xlim( (0, 15))