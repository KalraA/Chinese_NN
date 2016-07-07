from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers.recurrent import LSTM
from keras.optimizers import rmsprop
import numpy as np
model = Sequential()
model.add(LSTM(100, stateful=True, return_sequences=False, input_shape=(None, 3)))
model.add(Dense(3, input_dim=100))
model.add(Activation('softmax'))
model.compile(loss='categorical_crossentropy', optimizer='rmsprop')
import random
import math
#[rock, paper, scissors]
#[0.6, 0.2, 0.5] -> 0.6 -> 0 + 1 % 3

def mymax(lst):
	nlst = [0, 0, 0]
	nlst[0] = lst[0] + 0.5*lst[1] - lst[2]
	nlst[1] = lst[1] + 0.5*lst[2] - lst[0]
	nlst[2] = lst[2] + 0.5*lst[0] - lst[1]
	lst = nlst
	if lst[0] > lst[1] and lst[0] > lst[2]:
		return 0
	elif lst[1] > lst[2]:
		return 1
	else:
		return 2

answers = ['rock', 'paper', 'scissors']
i = 0
data = []
score = [0, 0]
final = answers[int(math.floor(random.random()*3) % 3)]
X_data = []
Y_data = []
while True:
	inp = raw_input()
	if inp == 'r' or inp == '3':
		data.append([1, 0, 0])
		inp = 'r'
	elif inp == 'p' or inp == '2':
		data.append([0, 1, 0])
		inp = 'p'
	elif inp == 's' or inp == '1':
		data.append([0, 0, 1])
		inp = 's'
	else:
		print score
		continue
	print final
	if (final == 'scissors' and inp == 'r') or (final == 'rock' and inp == 'p') or (final == 'paper' and inp == 's'):
		score[0] += 1
		print 'you win!!'
	elif (final == 'scissors' and inp == 'p') or (final == 'rock' and inp == 's') or (final == 'paper' and inp == 'r'):
		print 'I win!!'
		score[1] += 1
	else:
		print 'Tie'
	if i > 15:
		if i > 15:
			X_data.append(data[i-15:i])
			Y_data.append(data[i])
		# else:
		# X_data.append(data[:i:])
		# Y_data.append(data[i])
		# print np.array(X_data).shape
		# print np.array(X_data[1]).shape
		# print 'yo'
		model.fit(np.array(X_data), np.array(Y_data), batch_size=1024, nb_epoch = 10, validation_split=0)
		# if i > 15:
		# 	prediction = list(model.predict(np.array([data[-15::]]))[0])
		# else:
		prediction = list(model.predict(np.array([data]))[0])
		#print prediction
		final = answers[int((1 + mymax(prediction)) % 3)]
	else:
		final = answers[int(math.floor(random.random()*3) % 3)]
	i += 1;
