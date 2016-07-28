import numpy as np
from lol import array_of_chars
from keras.models import Sequential
from keras.layers import Dense, LSTM, Activation, Dropout
from keras.optimizers import rmsprop, adagrad
import json

array_of_chars = array_of_chars
infile = open('data.txt', 'r').read().decode('utf8')
X_data = np.zeros((422689, 1, 3716))
for c in range(422689):
	X_data[c][0][array_of_chars.index(ord(infile[c]))] = 1
time_steps = 1
batch_size = 32*7*3
epochs = 5
lahead = 1

print 'Making the Model'
model = Sequential()
model.add(GRU(512, batch_input_shape=(batch_size,time_steps, 3716),
	return_sequences=True, stateful=True))
model.add(Dropout('0.5'))
model.add(GRU(512, batch_input_shape=(batch_size,time_steps, 512),
	return_sequences=False, stateful=True))
model.add(Dropout('0.5'))
model.add(Dense(3716))
model.add(Activation('softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adagrad')
print 'Training the Model'
for i in range(5):
    model.fit(X_data[:-1:], np.reshape(X_data[1::], (422688, 3716)),
              batch_size=batch_size, nb_epoch=1, shuffle=False)
    model.reset_states()
    predicted = X_data[:672:, :, :]
    text = u''
    prediction = model.predict(predicted, batch_size=batch_size)
    print prediction.shape
    for j in range(len(prediction)):
    	text += unichr(array_of_chars[np.argmax(prediction[j])])
    print text

    json_string = model.to_json()
    open('my_model_architecture.json', 'w').write(json_string)
    model.save_weights('my_model_weights.h5', overwrite=True)


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
