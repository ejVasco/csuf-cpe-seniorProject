import torch
# this script is usefull to check if gpu i being detected for cuda processinlg
print(torch.version.cuda)
print(torch.cuda.is_available())
print(torch.cuda.get_device_name(0))

