import torch
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
from model import SimpleNet  # 确保这里和你之前改好的文件名一致

# 1. 加载测试教材（AI 没见过的新题）
transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))])
testset = torchvision.datasets.MNIST(root='./data', train=False, download=True, transform=transform)
testloader = torch.utils.data.DataLoader(testset, batch_size=5, shuffle=True)

# 2. 唤醒训练好的大脑
model = SimpleNet()
model.load_state_dict(torch.load('mnist_model.pth'))
model.eval() # 切换到“考试模式”

# 3. 抓 5 个数字来考试
dataiter = iter(testloader)
images, labels = next(dataiter)

# 4. 让 AI 答题
outputs = model(images)
_, predicted = torch.max(outputs, 1)

# 5. 展示结果
print("AI 答题卡：")
print(f"实际数字: {' '.join(str(labels[j].item()) for j in range(5))}")
print(f"预测结果: {' '.join(str(predicted[j].item()) for j in range(5))}")

# 画图直观看看
plt.figure(figsize=(10, 3))
for i in range(5):
    plt.subplot(1, 5, i+1)
    plt.imshow(images[i].numpy().squeeze(), cmap='gray')
    plt.title(f"AI Guess: {predicted[i]}")
    plt.axis('off')
plt.show()