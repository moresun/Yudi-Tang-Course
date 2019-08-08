import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['figure.figsize']=(10.0,8.0)
plt.rcParams['image.interpolation']='nearset'
plt.rcParams['image.cmap']='gray'

np.random.seed(0)
N=100
D=2
K=3
X=np.zeros((N*K,D))
y=np.zeros(N*K,dtype='uint8')
for j in range(K):
    ix=range(N*j,N*(j+1))
    r=np.linspace(0.0,1,N)
    t=np.linspace(j*4,(j+1)*4,N)+np.random.randn(N)*0.2
    X[ix]=np.c_[r*np.sin(t),r*np.cos(t)]
    y[ix]=j

h=100
W=0.01*np.random.randn(D,h)
b=np.zeros((1,h))
W2=0.01*np.random.randn(h,K)
b2=np.zeros((1,K))

step_size=1e-0
reg=1e-3

num_examples=X.shape[0]

for i in range(2000):
    hidden_layer= np.maximum(0,np.dot(X,W)+b)
    scores=np.dot(hidden_layer,W2)+b2
    scores=np.dot(X,W)+b
    exp_scores=np.exp(scores)
    probs=exp_scores/np.sum(exp_scores,axis=1,keepdims=True)

    corect_logprobs=-np.log(probs[range(num_examples),y])
    data_loss=np.sum(corect_logprobs)/num_examples
    reg_loss=0.5*reg*np.sum(W*W) +0.5*reg*np.sum(W2*W2)
    loss=data_loss+reg_loss
    if i%100==0:
        print("iteration %d: loss %f"%(i,loss))

    dscores=probs
    dscores[range(num_examples),y]-=1
    dscores/=num_examples

    dW2=np.dot(hidden_layer.T,dscores)
    db2=np.sum(dscores,axis=0,keepdims=True)

    dhidden=np.dot(dscores,W2)
    dhidden[hidden_layer<=0]=0

    dW=np.dot(X.T,dhidden)
    db=np.sum(dhidden,axis=0,keepdims=True)

    dW2+=reg*W2
    dW+=reg*W
    W+= -step_size*dW
    b+=-step_size*db
    W2+=-step_size*dW2
    b2+=-step_size*db2

hidden_layer=np.maximum(0,np.dot(X,W)+b)
scores=np.dot(hidden_layer,W2)+b2
predicted_class =np.argmax(scores,axis=1)
print('training accuracy : %.2f'%(np.mean(predicted_class==y)))
h=0.02
x_min ,x_max=X[:,0].min() -1,X[:,0].max() +1
y_min ,y_max=X[:,1].min() -1,X[:,1].max() +1
xx,yy=np.meshgrid(np.arange(x_min,x_max,h),
                  np.arange(y_min, y_max, h))
#Z=np.dot(np.c_[xx.ravel(),yy.ravel()],W)+b  #感觉h有问题，xx  yy出来也有问题，然后Z 无法reshape成，然后等高线画不出来
#Z=np.argmax(X,axis=1)
#Z=Z.reshape(xx.shape)
fig=plt.figure()
#plt.contourf(xx,yy,Z,cmap=plt.cm.Spectral,alpha=0.8)
plt.scatter(X[:,0],X[:,1],c=y,s=40,cmap=plt.cm.Spectral)
plt.xlim(xx.min(),xx.max())
plt.ylim(yy.min(),yy.max())
plt.show()
