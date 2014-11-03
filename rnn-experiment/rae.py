import time
import theano
import theano.tensor as T
import numpy         as np
from theano_toolkit import utils as U
from theano_toolkit import updates
from numpy_hinton import print_arr
from theano.printing import Print
from climin import adadelta
import cPickle
def unroll(final_rep,W1_i,W1_m,b2_m,b2_i,n_steps):
	def step(curr_rep,W1_m,b2_m,W1_i,b2_i):
		next_rep  = T.dot(curr_rep,W1_m.T) + b2_m
		input_rep = T.dot(curr_rep,W1_i.T) + b2_i
		return next_rep,input_rep
	[_,recon],_ = theano.scan(
			step,
			outputs_info = [final_rep,None],
			non_sequences  = [W1_m,b2_m,W1_i,b2_i],
			n_steps = n_steps
		)
	return recon


def make_rae(inputs,W1_i,W1_m,b_h,i_h,b2_m,b2_i):
	def step(inputs,hidden_1,W1_m,W1_i,b_h,b2_m,b2_i):
		hidden = T.tanh(T.dot(hidden_1,W1_m) +\
				T.dot(inputs,W1_i) +\
				b_h
                )
		reproduction_m = T.dot(hidden,W1_m.T) + b2_m
		reproduction_i = T.dot(hidden,W1_i.T) + b2_i

		return hidden,reproduction_m,reproduction_i

	[hidden_,reproduction_m_,reproduction_i_],_ = theano.scan(
                step,
                sequences     = [inputs],
                outputs_info  = [i_h,None,None],
                non_sequences = [W1_m,W1_i,b_h,b2_m,b2_i]
        )
	return hidden_,reproduction_m_,reproduction_i_

def build_network(input_size,hidden_size):
	X = T.dmatrix('X')
	W_input_to_hidden  = U.create_shared(U.initial_weights(input_size,hidden_size))
	W_hidden_to_hidden = U.create_shared(U.initial_weights(hidden_size,hidden_size))
	initial_hidden = U.create_shared(U.initial_weights(hidden_size), name='init_hidden')
	
	b_hidden              = U.create_shared(U.initial_weights(hidden_size))
	b_hidden_reproduction = U.create_shared(U.initial_weights(hidden_size))
	b_input_reproduction  = U.create_shared(U.initial_weights(input_size))

	parameters = [
			W_input_to_hidden,
			W_hidden_to_hidden,
			b_hidden,
			initial_hidden,
			b_hidden_reproduction,
			b_input_reproduction,
		]

	hidden, hidden1_reproduction, input_reproduction = make_rae(
			X,
			W_input_to_hidden,
			W_hidden_to_hidden,
			b_hidden,
			initial_hidden,
			b_hidden_reproduction,
			b_input_reproduction
		)

	unrolled = unroll(
			hidden[-1],
			W_input_to_hidden,
			W_hidden_to_hidden,
			b_hidden_reproduction,
			b_input_reproduction,
			hidden.shape[0]
		)

	return X,parameters,hidden,hidden1_reproduction,input_reproduction,unrolled


def build_error(X,hidden,hidden1_reproduction,input_reproduction):
	input_reproduction_sqerror  = T.mean((X - input_reproduction)**2)
	hidden_reproduction_sqerror = T.mean((hidden[:-1] - hidden1_reproduction[1:])**2)
	return input_reproduction_sqerror + hidden_reproduction_sqerror


def train_model(docs, wordvec_size,hidden_size, error_threshold, update_mu = 1e-3, update_eps = 0.95):
	X,parameters,hidden,hidden1_reproduction,input_reproduction,unrolled = build_network(wordvec_size, hidden_size)

	#hidden, hidden_rep, input_rep, unrlld  = f(docs)

	error = build_error(X,hidden,hidden1_reproduction,input_reproduction)
	cost  = error # + 1e-6*sum( T.sum(abs(p)) for p in parameters )
	gradients = T.grad(cost,wrt=parameters)
	
	eps = T.dscalar('eps')
	mu  = T.dscalar('mu')
	
	train = theano.function(
			inputs = [X, eps, mu],
			updates = updates.adadelta(parameters, gradients, mu, eps),
			outputs = error
		)

	error = 10
        count = 0
	for i in range(10):
                start_time = time.time()
                error = 0
                for doc in docs:
                        error += train(doc, update_mu, update_eps)
                if count % 1 == 0:
                        print "iter=%d" % count,time.time() - start_time, error / len(docs)
                count += 1

	f = theano.function(
                inputs  = [X],
                outputs = [hidden,hidden1_reproduction,input_reproduction,unrolled])
        print "Finish count=%d error=%f" % (count, error)
        return f
#        return parameters, hidden, hidden1_reproduction, input_reproduction
#def predict():
#	f = theano.function(
#			inputs  = [X],
#			outputs = [hidden,hidden1_reproduction,input_reproduction,unrolled]
#		)

if __name__ == '__main__':
        example = np.array([[[0.1,0.2,0.3,0.2,0.5,0.6,0.7,0.8],[0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]]])
        f = file('obj.save', 'rb')
        #cPickle.dump(f, train_model(example, 8, 8, 0.001))
        xx = train_model(example, 8, 8, 0.0001)
        #cPickle.dump(xx, f)
        
        _, _, inp, _ = xx(example)
        print inp

        #print "Load model finish"
        #_, _, inp, _ = xx(example)

	#print_arr(example)
	#print_arr(unrolld)
	#print_arr(parameters[1].get_value())
