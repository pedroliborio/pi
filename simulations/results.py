import matplotlib.pyplot as plt
import numpy as np
import os
import math

def ConfidenceInterval(values):
    N = len(values)
    Z = 1.96
    std_dev = np.std(values)
    std_error = std_dev / math.sqrt(N)
    return Z * std_error



config = 'General'
scenario = 'MyScenario'
seeds = 10
totVehicles = [100,200,300,400]
filesPath = 'results/'

listCoverage = [[] for n in range(len(totVehicles))]
listTransmissions = [[] for n in range(len(totVehicles))]

transmissions = float(0)
coverage = float(0)

plotCoverage = list()
plotCoverageCI = list()
plotTransmission = list()
plotTransmissionCI = list()


for i in range(0,len(totVehicles)):
	for seed in range(0,seeds):
		
		transmissions = 0.0
		coverage = 0.0

		fileName = filesPath+config+'-'+str(seed)+'-'+str(totVehicles[i])+'.sca'
		
		with open(fileName,'r') as fileResults:

			lines = fileResults.readlines()
			
			
			for line in lines:
				splitedLine = line.split(' ')
				if splitedLine[0] == 'scalar':

					if splitedLine[1] == '.':
						continue
					else:
						if splitedLine[1].split('.')[2] == 'appl':
							if splitedLine[2] == '\tgeneratedWSMs':
								transmissions+= float(splitedLine[3])		
							else:
								if splitedLine[2] == '\treceivedWSMs':
									receivedWSMs = float(splitedLine[3])
									if receivedWSMs > 0:
										coverage+=1

		listTransmissions[i].append(transmissions)
		listCoverage[i].append(coverage)


print(listTransmissions)
print(listCoverage)

for i in range(0,len(totVehicles)):
	
	#Compute Coverage
	listCoverage[i] = np.divide(listCoverage[i],totVehicles[i])
	listCoverage[i] = np.multiply(listCoverage[i],100)
	
	plotCoverage.append(np.mean(listCoverage[i]))
	plotCoverageCI.append(ConfidenceInterval(listCoverage[i]))

	plotTransmission.append(np.mean(listTransmissions[i]))
	plotTransmissionCI.append(ConfidenceInterval(listTransmissions[i]))



fig, (ax0, ax1) = plt.subplots(nrows=2, sharex=True)
ax0.errorbar(totVehicles, plotCoverage, yerr=plotCoverageCI, color='r', marker='H')
ax0.grid(True)
ax0.set_xlabel('# Vehicles')
ax0.set_ylabel('Coverage (%)')
ax0.set_ylim([0,100])
ax0.set_xlim([90,410])
ax0.set_xticks(totVehicles)



ax1.errorbar(totVehicles, plotTransmission, yerr=plotTransmissionCI, color='g', marker='D')
ax1.grid(True)
ax1.set_xlabel('# Vehicles')
ax1.set_ylabel('# Transmissions')
ax1.set_xticks(totVehicles)

fig.savefig("PI_BASICO.png", dpi=200)

plt.show()