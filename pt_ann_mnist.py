import torch
import torchvision
import torchvision.transforms as transform
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score

training_data = torchvision.datasets.MNIST(root="",download=True,train=True,transform=transform.ToTensor())
testing_data = torchvision.datasets.MNIST(root="",download=True,train=False,transform=transform.ToTensor())

train_load = DataLoader(training_data,batch_size=20,shuffle=True,num_workers=5)
test_load = DataLoader(testing_data,batch_size=20,shuffle=True,num_workers=5)

#Hyperparameters:
learning_rate=0.01
input_size = 28*28
num_classes=10
n_iters=3

class FeedForwardNet(nn.Module):
  def __init__(self,input_size,num_classes,hidden_size):
    super(FeedForwardNet,self).__init__()
    self.l1 = nn.Linear(input_size,hidden_size)
    self.relu = nn.ReLU()
    self.l2 = nn.Linear(hidden_size,num_classes)

  def forward(self,x):
    out = self.l1(x)
    out = self.relu(out)
    out = self.l2(out)
    return out

model = FeedForwardNet(input_size,num_classes,hidden_size=100)
loss = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(),lr=learning_rate)

len(train_load)

#Training Loop
for epoch in range(n_iters):
  for i, (data, labels) in enumerate(train_load):
    y_pred = model(data.reshape(-1,28*28))
    l = loss(y_pred,labels)
    l.backward()
    optimizer.step()
    optimizer.zero_grad()
    if i % 500 == 0:
      print(f"Epoch:{epoch+1} n:{i+500}/{len(train_load)}, loss:{l}")

with torch.no_grad():
  pred=[]
  act=[]
  for i, (data,labels) in enumerate(test_load):
    y_pred = model(data.reshape(-1,28*28))
    _,y_pred = torch.max(y_pred,1)
    pred +=y_pred
    act +=labels

print(accuracy_score(pred,act))
