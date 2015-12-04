import time, sys, csv
import algolib
from xml.dom.minidom import parse

'''
	python module solving fitst task
'''

def readFromXML(inputFile) :

	'''
		read from xml
	'''

	dom = parse(inputFile)
	nets = dom.getElementsByTagName('net')
	resistors = dom.getElementsByTagName('resistor')
	capactors = dom.getElementsByTagName('capactor')
	diodes = dom.getElementsByTagName('diode')
	return { 'nets':nets, 'resistors':resistors, 'capactors':capactors, 'diodes':diodes }

def writeToCsv(outputFile, matrix):

	'''
		write to csv
	'''

	csvfile = open(outputFile, 'w', newline='')
	csvWriter = csv.writer(csvfile, delimiter=',')
	for m in matrix :
		csvWriter.writerow([round(m[i], 7) for i in range(len(m))])


def runAlgo(inputFile, outputFile) :

		'''
			running main algo
		'''

		start = time.process_time()

		matrix = []
		elems = readFromXML(inputFile)
		for j in range(len(elems['nets'])) : matrix.append([0 for i in range(len(elems['nets']))])

		def addToMatrix(attrs, diode):
			prev = matrix[int(attrs['net_from'].value)-1][int(attrs['net_to'].value)-1]
			next = float(attrs['resistance'].value)
			matrix[int(attrs['net_from'].value)-1][int(attrs['net_to'].value)-1] = prev*next/(prev+next) if prev > 0 else next

			prev = matrix[int(attrs['net_to'].value)-1][int(attrs['net_from'].value)-1]
			next = float(attrs['reverse_resistance'].value) if diode else float(attrs['resistance'].value)
			matrix[int(attrs['net_to'].value)-1][int(attrs['net_from'].value)-1] = prev*next/(prev+next) if prev > 0 else next
				
		for resistor in elems['resistors'] : addToMatrix(resistor.attributes, False)
		for capactor in elems['capactors'] : addToMatrix(capactor.attributes, False)
		for diode in elems['diodes'] : addToMatrix(diode.attributes, True)

		matrix = algolib.FloydWarshellBasedAlgo(matrix)

		writeToCsv(outputFile, matrix)

		end = time.process_time()
		print("Python calculations time: {:.0f} msec".format(1000*(end-start)))


if __name__ == "__main__" :
	if len(sys.argv) != 3 :
		print("Usage {0} input.xml output.csv".format(sys.argv[0]))
	else :
		inputFile, outputFile = sys.argv[1], sys.argv[2]
		runAlgo(inputFile, outputFile)
