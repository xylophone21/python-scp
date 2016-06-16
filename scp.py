"""
A python implementation for Set Cover Problem with weight.
See http://pages.cs.wisc.edu/~shuchi/courses/880-S07/scribe-notes/lecture03.pdf for details
"""
import random
import json
import copy

def scp_cli(str):
	if False:
		print(str)

def scp_log(str):
	if False:
		print(str)

def scp_v(str):
	if False:
		print(str)

#Fixme: random S may has no solution
def generate_random_S(key_count,value_count,s_count,si_count_min,si_count_max,si_weight_max):
	E = []
	for i in range(0,key_count):
		for j in range(0,value_count):
			E.append("key"+str(i)+"="+str(j))

	scp_v(E)

	S = []
	for i in range(0,s_count):
		id = i+1
		si_count = random.randint(si_count_min, si_count_max)
		si = random.sample(E,si_count)
		S.append({"id":id,"si":si,"weight":random.randint(1, si_weight_max)})
	scp_v(json.dumps(S,indent=1))
	return S

def fill_addion_info_sc(S):
	E = []
	for si in S:
		for ei in si["si"]:
			if ei not in E:
				E.append(ei)

	E.sort()
	sc = {"E":E,"S":S}
	scp_v(sc)
	return sc

def format_sc(sc):
	Sset = []
	for si in sc["S"]:
		siset = copy.deepcopy(si)
		siset["si"] = set(siset["si"])
		Sset.append(siset)

	scset = {"E":set(sc["E"]),"S":Sset}
	scp_v(scset)

	return scset

def calculate_wsp_value(x,Es):
	s = x["si"] & Es
	scp_log("X & Es = " + str(s))
	return len(s)/x["weight"]

def scp(sc):
	C = set([])
	E = set(sc["E"])
	Es = set(sc["E"])
	S = sc["S"]
	SIdx = set(range(0,len(S)))

	while len(Es) != 0:
		maxvalue = 0
		maxvalueIndex = -1
		scp_log("Finding Es = " + str(Es))
		scp_log("")
		for xIdx in SIdx:
			scp_log("Judge S" + str(xIdx) + " = " + str(S[xIdx]))
			value = calculate_wsp_value(S[xIdx],Es)
			scp_log(value)
			if value > maxvalue:
				maxvalue = value
				maxvalueIndex = xIdx
			scp_log("")

		assert(maxvalueIndex >= 0 and maxvalue > 0)
		scp_log("Found Si(" + str(maxvalueIndex) + ") = " + str(S[maxvalueIndex]))

		s = set([maxvalueIndex])
		C = C | s
		SIdx = SIdx - s
		Es = Es - set(S[maxvalueIndex]["si"])

		scp_log("Got C = " + str(C))
		scp_log("Got SIdx = " + str(SIdx))
		scp_log("Got Es = " + str(Es))
		scp_log("")

	Clist = list(C)
	Clist.sort()
	return Clist

def check_scp(sc,c):
	E = sc["E"]
	Es = set([])

	W = 0
	for xIdx in c:
		Es |= set(sc["S"][xIdx]["si"])
		W += sc["S"][xIdx]["weight"]

	scp_log("W = " + str(W))
	assert(Es == E)

def main():
	S = generate_random_S(10,3,10,3,8,100)

	#import SData
	#S = SData.get_S()

	print(json.dumps(S,indent=1))

	sc = fill_addion_info_sc(S)
	#scp_cli(json.dumps(sc,indent=1))

	sc = format_sc(sc)
	scp_cli(sc)

	C = scp(sc)
	print("Found C = " + str(C))
	print("Count = " + str(len(C)))
	print("")

	check_scp(sc,C)


if __name__ == '__main__':
	main()

