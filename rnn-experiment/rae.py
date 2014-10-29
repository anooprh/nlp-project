import theano
import theano.tensor as T
import numpy         as np
from theano_toolkit import utils as U
from theano_toolkit import updates
from numpy_hinton import print_arr
from theano.printing import Print
from climin import adadelta

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


def train_model():
        pass
def predict():
        pass

if __name__ == '__main__':
	X,parameters,hidden,hidden1_reproduction,input_reproduction,unrolled = build_network(8,64)
	f = theano.function(
			inputs  = [X],
			outputs = [hidden,hidden1_reproduction,input_reproduction,unrolled]
		)

	error = build_error(X,hidden,hidden1_reproduction,input_reproduction)
	cost  = error # + 1e-6*sum( T.sum(abs(p)) for p in parameters )
	gradients = T.grad(cost,wrt=parameters)
	
	eps = T.dscalar('eps')
	mu  = T.dscalar('mu')
	
	train = theano.function(
			inputs = [X,eps,mu],
			updates = updates.adadelta(parameters,gradients,mu,eps),
			outputs = error
		)

	#example = np.vstack((np.eye(8),np.eye(8)))
	example = np.eye(8)
	error = 10
	lr = 0.0001
	t = 0
        count = 0
	while error > 0.0001:
		error = train(example,1e-6,0.95)
		#error = train(example,lr,0)
                count += 1
		if count % 100 == 0:
                        print count,error
		t += 1
		
	

	np.random.shuffle(example)
	hidden, hidden_rep, input_rep, unrlld  = f(example)

	print_arr(example)
	print_arr(unrlld)
	print_arr(parameters[1].get_value())
#	print_arr(unrlld,hidden)
