import pyssp4sim
import matplotlib


sim = pyssp4sim.Simulator("./build/results/config.json")
sim.init()
sim.simulate()

