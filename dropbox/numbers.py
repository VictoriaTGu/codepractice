d = {1: "one", 2: "two", 3: "three"} 
dtens = {1: "ten", 2: "twenty", 3: "thirty"}
level = {1: None, 2: "thousand", 3: "million"}

def convert_three_digits(number):
	s = ""
	ones = number % 10
	if ones != 0:
		s += d[ones] 
	tens = (number % 100 - ones) / 10
	if tens != 0:
		s += 
	hundreds = (number % 1000 - tens*10 - ones) / 100
	s = d[hundreds] + " hundred " + dtens[tens] + " " + d[ones]
	return s

def convert_main(number):
	level_n = 1
	s = ""
	while number > 1000 and level_n < 4:
		three_digits = number % 1000
		s += convert_three_digits(three_digits)
		if level_n in level:
			s += " " + level[level_n]
		level += 1
		number = number / 1000
	s += convert_three_digits(number)
	return s
	

print convert_main(4321)
	
