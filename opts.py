import svgcuts
import math

unit = "in"
edge = 0.688
rows = 7
pad = 0.15

squares = [
	('L', 'T')
]
squares = squares * 110
squares += ([(' ', ' ')] * (rows - len(squares) % rows)) # padding squares, make it so we get a rectangle of them

vals = {
	'A' : 2,
	'L' : 4,
	'T' : 1,
	'*' : 0,
	' ' : 0 # no-op padding squares
}

cols = int(math.ceil(float(len(squares)) / float(rows)))

def n2params(n, flip) :
	x = n // rows
	y = n % rows
	if flip :
		y = rows - y

	main = squares[n][0]
	rev = squares[n][0]
	
	if flip :
		main,rev = rev,main

	value = vals[main]

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
	pass

pattern.write('pattern.svg')
a.write('a.svg')
