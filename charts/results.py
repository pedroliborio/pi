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
filesPath = '../simulations/results/'

listCoverage = [[] for n in range(len(totVehicles))]
listTransmissions = [[] for n in range(len(totVehicles))]
listDelay = [[] for n in range(len(totVehicles))]
listColision = [[] for n in range(len(totVehicles))]

transmissions = float(0)
coverage = float(0)
receivedWSMsToPlot = float(0)
delaySum = float(0)
totalColision = float(0)

plotCoverage = list()
plotCoverageCI = list()
plotTransmission = list()
plotTransmissionCI = list()
plotDelay = list()
plotDelayCI = list()
plotColision = list()
plotColisionCI  = list()


for i in range(0,len(totVehicles)):
	for seed in range(0,seeds):
		
		transmissions = 0.0
		coverage = 0.0
		receivedWSMsToPlot = 0.0
		delaySum = 0.0
		totalColision = 0.0

		fileName = filesPath+config+'-'+str(seed)+'-'+str(totVehicles[i])+'.sca'
		
		with open(fileName,'r') as fileResults:

			lines = fileResults.readlines()
			
			
			for line in lines:
				splitedLine = line.split(' ')
				if splitedLine[0] == 'scalar':

					if splitedLine[1] == '.':
						continue
					else:
						#appl metrics
						if splitedLine[1].split('.')[2] == 'appl':
							if splitedLine[2] == '\tgeneratedWSMs':
								transmissions+= float(splitedLine[3])		
							else:
								if splitedLine[2] == '\treceivedWSMs':
									receivedWSMs = float(splitedLine[3])
									receivedWSMsToPlot += receivedWSMs
									if receivedWSMs > 0:
										coverage+=1
								else:
									if splitedLine[2] == '\tdelaySum':
										delaySum+= float(splitedLine[3])
						else:
							#nic metrics 
							if splitedLine[1].split('.')[2] == 'nic':
								if splitedLine[2] == '\tTotalLostPackets':
									totalColision += float(splitedLine[3])

		listTransmissions[i].append(transmissions)
		listCoverage[i].append(coverage)
		listDelay[i].append(delaySum/receivedWSMsToPlot)
		listColision[i].append(totalColision)


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

	plotDelay.append(np.mean(listDelay[i]))
	plotDelayCI.append(ConfidenceInterval(listDelay[i]))

	#colisions per vehicles
	listColision[i] = np.divide(listColision[i],totVehicles[i])
	plotColision.append(np.mean(listColision[i]))
	plotColisionCI.append(ConfidenceInterval(listColision[i]))






fig = plt.figure(figsize=(6, 4))
sub1 = fig.add_subplot(221) # instead of plt.subplot(2, 2, 1)
#sub1.set_title('The function f') # non OOP: plt.title('The function f')
sub1.errorbar(totVehicles, plotCoverage, yerr=plotCoverageCI, color='r', marker='H')
sub1.set_xlabel('Density (veh/km²)')
sub1.set_ylabel('Coverage (%)')
sub1.grid(True)
sub1.set_ylim([0,100])
sub1.set_xlim([90,410])
sub1.set_xticks(totVehicles)


sub2 = fig.add_subplot(222)
sub2.errorbar(totVehicles, plotTransmission, yerr=plotTransmissionCI, color='r', marker='H')
sub2.grid(True)
sub2.set_xlim([90,410])
sub2.set_xlabel('Density (veh/km²)')
sub2.set_ylabel('Number of Transmissions')
sub2.set_xticks(totVehicles)


sub3 = fig.add_subplot(223)
sub3.errorbar(totVehicles, plotDelay, yerr=plotDelayCI, color='r', marker='H')
sub3.grid(True)
sub3.set_xlim([90,410])
sub3.set_xlabel('Density (veh/km²)')
sub3.set_ylabel('Average Delay (s)')
sub3.set_xticks(totVehicles)

sub4 = fig.add_subplot(224)
sub4.errorbar(totVehicles, plotColision, yerr=plotColisionCI, color='r', marker='H')
sub4.grid(True)
sub4.set_xlim([90,410])
sub4.set_xlabel('Density (veh/km²)')
sub4.set_ylabel('Collisions (per vehicle)')
sub4.set_xticks(totVehicles)

#markers =  H, g, 0, *



#fig, (ax0, ax1, ax2, ax3) = plt.subplots(nrows=4, ncols=2, sharex=True)

# ax0.errorbar(totVehicles, plotCoverage, yerr=plotCoverageCI, color='r', marker='H')
# ax0.grid(True)
# ax0.set_xlabel('Number of Vehicles')
# ax0.set_ylabel('Coverage (%)')
# ax0.set_ylim([0,100])
# ax0.set_xlim([90,410])
# ax0.set_xticks(totVehicles)



# ax1.errorbar(totVehicles, plotTransmission, yerr=plotTransmissionCI, color='g', marker='D')
# ax1.grid(True)
# ax1.set_xlabel('Number of Vehicles')
# ax1.set_ylabel('Number of Transmissions')
# ax1.set_xticks(totVehicles)


# ax2.errorbar(totVehicles, plotDelay, yerr=plotDelayCI, color='m', marker='o')
# ax2.grid(True)
# ax2.set_xlabel('Number of Vehicles')
# ax2.set_ylabel('Average Delay (s)')
# ax2.set_xticks(totVehicles)

fig.savefig("PI_BASICO.png", dpi=300)

plt.show()


