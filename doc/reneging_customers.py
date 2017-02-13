import simpy
import random

def reneging_customer_proc(env, name, patience, queue, reneged):
    queue.append(name) # Customers are identified by name, so all names should be unique
    yield env.timeout(1.3)
    if name in queue:
        queue.remove(name)
        reneged.append( env.now ) # Record the time of the reneg 

def customer_generator_proc(env, numberOfCustomers, timeBetween, patience, reneged, queue, newArrivalEvents):
    """ Will generate a fixed number of customers, with random time between arrivals."""
    k = 0
    while k<numberOfCustomers:
        yield env.timeout( random.expovariate(1.0/timeBetween) )
        k += 1
        env.process( reneging_customer_proc(env, name = "Customer-%d" %k, patience = patience, queue = queue, reneged = reneged) )
        while newArrivalEvents != []:
            ev = newArrivalEvents.pop(0)
            # The newArrivalEvents list contains events that servers are waiting for in order to proceed.
            # What they are waiting for is for a new customer to arrive, so trigger the event
            ev.succeed()

def service_proc(env, serviceTime, queue, arrivalEvents):
    while True:
        while queue != []:
            customer = queue.pop(0) # Take out the first customer
            yield env.timeout( random.expovariate(1.0/serviceTime) )
        newArrivalEv = env.event()
        arrivalEvents.append(newArrivalEv) 
        yield newArrivalEv # Wait for the arrival event to be triggered. This is done in customer_generator_proc

N = 4000 # Number of customers to simulate
env = simpy.Environment()
queue = []
waitingForArrivalEvents = []
reneged = []
env.process( service_proc(env, 1.3, queue, waitingForArrivalEvents) )
env.process( customer_generator_proc(env, N, 0.8, 1.3, reneged, queue, waitingForArrivalEvents) )

env.run()

print( "Estimated probability of customer reneging: p = %f, based on %d observations" % ( len(reneged)/N, N) ) 
