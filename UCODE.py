import json


dictionary = { 
	'00': '\u200c',
	'01': '\u200d',
	'10': '\u2060',
	'11': '\u2062'
}


def to_binary(data):
	str_data = json.dumps(data)
	return ' '.join('{0:08b}'.format(ord(x), 'b') for x in str_data)


def to_str(data):
	json_dict = ''.join(chr(int(x, 2)) for x in data.split())
	return json.loads(json_dict)


def u_encode(data):
	# Convert data to binary for easy encoding
	bin_data = to_binary(data)

	new_bin_list = []
	for w in bin_data.split():
		new_bin_str = ''
		for l in range(0, len(w), 2):
			new_bin_str += dictionary[w[l:l+2]]
		new_bin_list.append(new_bin_str)
	return ''.join(new_bin_list)


def u_decode(data):
	to_decode = data.split()[-1]
	u_list = [to_decode[l:l+4] for l in range(0, len(to_decode), 4)]

	bin_u_list = []
	for l in u_list:
		new_l = l.replace('\u200c', '00').replace('\u2060', '10').replace('\u200d', '01').replace('\u2062','11')
		bin_u_list.append(new_l)

	decoded_bin = ' '.join(bin_u_list)
	return to_str(decoded_bin)
