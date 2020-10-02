import AES256
import UCODE


def hide(secret, password, hide_text):
	encrypted_dict = AES256.encrypt(secret, password)
	u_encoded_dict = UCODE.u_encode(encrypted_dict)
	return u_encoded_dict + hide_text


def reveal(plain_text, password):
	# Extracting secret data
	for i in range(len(plain_text)):
		if ord(plain_text[i]) not in [8290, 8205, 8288, 8204]:
			data = plain_text[:i]
			break

	u_decoded_dict = UCODE.u_decode(data)
	decrypted_text = AES256.decrypt(u_decoded_dict, password)
	return decrypted_text
