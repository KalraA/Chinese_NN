import numpy as np
from array import array_of_chars
from keras.models import Sequential
from keras.layers import Dense, LSTM, Activation, Dropout
from keras.optimizers import rmsprop
import json

array_of_chars = array_of_chars
infile = open('data.txt', 'r').read().decode('utf8')
X_data = np.zeros((422689, 3716))
for c in range(422689):
	X_data[c][array_of_chars.index(ord(infile[c]))] = 1
Y_data = X_data[1::]
time_steps = 10
batch_size = 1
epochs = 5
lahead = 1

print 'Making the Model'
model = Sequential()
model.add(LSTM(32, batch_input_shape=(batch_size,time_steps, 3716),
	return_sequences=True, stateful=True))
model.add(Dropout('0.5'))
model.add(LSTM(32, batch_input_shape=(batch_size,time_steps, 32)
	return_sequences=False, stateful=True))
model.add(Dropout('0.5'))
model.add(Dense(3716))
model.add(Activation('softmax'))
model.compile(loss='categorical_crossentropy', optimizer='rmsprop')
X_data = np.array([X_data[::-1]])

print 'Training the Model'
for i in range(200):
    print 'epochs: ' + str(i)
    for j in range(422689-timesteps):
	    print j
	    model.train_on_batch(X_data[:, j:j+100, :],
	              np.reshape(X_data[:, j+100, :], (1, 3716)))
    model.reset_states()
    predics = X_data[:, :100:, :]
    text = u''
    for i in range(300):
    	predicted = model.predict(predics[:, :100:, :], batch_size=batch_size)
    	predics = np.array([np.concatenate((predics[0], predicted), axis=0)])
    	text += unichr(array_of_chars[np.argmax(predicted[0])])
    print text

json_string = model.to_json()
open('my_model_architecture.json', 'w').write(json_string)
model.save_weights('my_model_weights.h5')


# a b c aa bb cc ab ac cb abc
# [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# aaabbabbccbca - >

# for c in infile:
# 	int_value = ord(c)
# 	if int_value not in array_of_chars:
# 		array_of_chars.append(int_value)

# outfile = open('array.py', 'w')
# outfile.write('array_of_chars = ')
# outfile.write(str(array_of_chars))