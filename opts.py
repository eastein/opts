import svgcuts
import math

unit = "in"
edge = 0.688
rows = 7
pad = 0.15

squares = [
	('E', 'A'),
	('E', 'A'),
	('I', 'A'),
	('I', 'A'),
	('O', 'A'),
	('O', 'A'),
	('U', 'A'),
	('R', 'A'),
	('D', 'B'),
	('F', 'B'),
	('P', 'B'),
	('P', 'B'),
	('E', 'C'),
	('N', 'C'),
	('M', 'C'),
	('M', 'C'),
	('W', 'C'),
	('G', 'D'),
	('G', 'D'),
	('M', 'D'),
	('N', 'D'),
	('S', 'D'),
	('T', 'D'),
	('A', 'E'),
	('A', 'E'),
	('H', 'E'),
	('I', 'E'),
	('I', 'E'),
	('L', 'E'),
	('N', 'E'),
	('O', 'E'),
	('S', 'E'),
	('T', 'E'),
	('K', 'F'),
	('P', 'F'),
	('E', 'G'),
	('N', 'G'),
	('E', 'H'),
	('L', 'H'),
	('N', 'H'),
	('R', 'H'),
	('T', 'H'),
	('A', 'I'),
	('E', 'I'),
	('E', 'I'),
	('L', 'I'),
	('N', 'I'),
	('O', 'I'),
	('O', 'I'),
	('R', 'I'),
	('X', 'K'),
	('K', 'J'),
	('T', 'L'),
	('R', 'L'),
	('T', 'M'),
	('W', 'M'),
	('W', 'M'),
	('E', 'N'),
	('S', 'N'),
	('S', 'N'),
	('T', 'N'),
	('Y', 'N'),
	('A', 'O'),
	('A', 'O'),
	('I', 'O'),
	('E', 'O'),
	('L', 'O'),
	('T', 'O'),
	('U', 'O'),
	('V', 'P'),
	('V', 'P'),
	('*', 'Q'),
	('E', 'R'),
	('D', 'R'),
	('H', 'R'),
	('L', 'R'),
	('N', 'R'),
	('O', 'R'),
	('T', 'R'),
	('E', 'S'),
	('G', 'S'),
	('H', 'S'),
	('N', 'S'),
	('M', 'S'),
	('T', 'S'),
	('A', 'T'),
	('C', 'T'),
	('E', 'T'),
	('H', 'T'),
	('I', 'T'),
	('L', 'T'),
	('N', 'T'),
	('O', 'T'),
	('S', 'T'),
	('A', 'U'),
	('E', 'U'),
	('O', 'U'),
	('W', 'V'),
	('S', 'W'),
	('*', 'X'),
	('E', 'Y'),
	('J', '*'),
	('Z', '*'),
	('V', 'Z'),
	('I', 'M'),
	('L', 'E'),
	('O', 'L'),
	('V', 'O'),
	('E', 'D'),
	('U', 'Y')
]

squares += ([(' ', ' ')] * (rows - len(squares) % rows)) # padding squares, make it so we get a rectangle of them

vals = {
	'A' : 2,
	'L' : 4,
	'T' : 1,
	'E' : 1,
	'U' : 5,
	'O' : 2,
	'C' : 5,
	'H' : 4,
	'I' : 2,
	'X' : 9,
	'Y' : 7,
	'J' : 8,
	'N' : 2,
	'S' : 3,
	'W' : 5,
	'V' : 7,
	'Z' : 9,
	'D' : 4,
	'R' : 3,
	'P' : 6,
	'B' : 6,
	'F' : 6,
	'G' : 5,
	'K' : 8,
	'M' : 5,
	'Q' : 9,
	'*' : 0,
	' ' : 0 # no-op padding squares
}

cols = int(math.ceil(float(len(squares)) / float(rows)))

def n2params(n, flip) :
	x = n // rows
	y = n % rows
	if flip :
		y = rows - y - 1

	main = squares[n][0]
	rev = squares[n][1]
	
	if flip :
		main,rev = rev,main

	try :
		value = vals[main]
	except KeyError :
		print 'value unk for %s, zeroing' % main	
		value = 0

	return {
		'x' : x,
		'y' : y,
		'main' : main,
		'rev' : rev,
		'value' : value
	}

pattern = svgcuts.Layer(24, 12, unit=unit)
a = svgcuts.Layer(24, 12, unit=unit)
b = svgcuts.Layer(24, 12, unit=unit)

# make pattern

xd = pad * 2 + edge * cols
yd = pad * 2 + edge * rows

ps = [
	svgcuts.Point(pad, pad),
	svgcuts.Point(pad, pad + yd),
	svgcuts.Point(pad + xd, pad + yd),
	svgcuts.Point(pad + xd, pad)
]

for n in range(4) :
	pattern.add_line(svgcuts.Line(ps[n], ps[(n + 1) % 4], unit=unit))

# make squares

# position an identity corner (upper left corner of a square)

def xy2p(x, y, xadg=0.0, yadg=0.0) :
	_x = pad + x * edge + xadg
	_y = pad + y * edge + yadg
	return svgcuts.Point(_x, _y)

for x in range(cols) :
	for y in range(rows) :
		if y == 0 :
			a.add_line(svgcuts.Line(xy2p(x, y), xy2p(x + 1, y), unit=unit))
		if x == 0 :
			a.add_line(svgcuts.Line(xy2p(x, y), xy2p(x, y + 1), unit=unit))

		a.add_line(svgcuts.Line(xy2p(x + 1, y), xy2p(x + 1, y + 1), unit=unit))
		a.add_line(svgcuts.Line(xy2p(x, y + 1), xy2p(x + 1, y + 1), unit=unit))

for n in range(len(squares)) :
	# put in writing

	for layer, flip in [(a, False), (b, True)] :
		params = n2params(n, flip)
		# main letter
		mp = xy2p(params['x'], params['y'], xadg=edge * .395, yadg = edge * .66)
		layer.add_text(mp.x, mp.y, params['main'], fontsize=22)

		rp = xy2p(params['x'], params['y'], xadg=edge * .125, yadg = edge * .33)
		layer.add_text(rp.x, rp.y, params['rev'], fontsize=13)

		vp = xy2p(params['x'], params['y'], xadg=edge * .735, yadg = edge * .33)
		layer.add_text(vp.x, vp.y, str(params['value']), fontsize=13)

pattern.write('pattern.svg')
a.write('a.svg')
b.write('b.svg')
