import algolib, time, sys, csv
from xml.dom.minidom import parse

if __name__ == "__main__" :
	if len(sys.argv) != 3 :
		print("Usage {0} input.xml output.csv".format(sys.argv[0]))
	else :
		inputFile, outputFile = sys.argv[1], sys.argv[2]
		start = time.process_time()

		#read from xml
		dom = parse(inputFile)
		nets = dom.getElementsByTagName('net')
		resistors = dom.getElementsByTagName('resistor')
		capactors = dom.getElementsByTagName('capactor')
		diodes = dom.getElementsByTagName('diode')

		#fill init matrix
		matrix = []
		for j in range(len(nets)) : matrix.append([0 for i in range(len(nets))])

		def addToMatrix(attrs, diode):
			prev = matrix[int(attrs['net_from'].value)-1][int(attrs['net_to'].value)-1]
			next = float(attrs['resistance'].value)
			matrix[int(attrs['net_from'].value)-1][int(attrs['net_to'].value)-1] = prev*next/(prev+next) if prev > 0 else next

			prev = matrix[int(attrs['net_to'].value)-1][int(attrs['net_from'].value)-1]
			next = float(attrs['reverse_resistance'].value) if diode else float(attrs['resistance'].value)
			matrix[int(attrs['net_to'].value)-1][int(attrs['net_from'].value)-1] = prev*next/(prev+next) if prev > 0 else next
				

		for resistor in resistors : addToMatrix(resistor.attributes, False)
		for capactor in capactors : addToMatrix(capactor.attributes, False)
		for diode in diodes : addToMatrix(diode.attributes, True)

		#run algo
		matrix = algolib.FloydWarshellBasedAlgo(matrix)

		end = time.process_time()

		#write to csv
		csvfile = open(outputFile, 'w', newline='')
		csvWriter = csv.writer(csvfile, delimiter=',')
		for m in matrix :
			csvWriter.writerow([round(m[i], 7) for i in range(len(m))])
		print("Python calculations time: {:.0f} msec".format(1000*(end-start)))
