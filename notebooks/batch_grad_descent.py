import numpy as np
import matplotlib.pyplot as plt

rate = 0.05  # learning rate


def da(y, y_p, x):
    return (y - y_p) * (-x)


def db(y, y_p):
    return (y - y_p) * (-1)


def calc_loss(a, b, x, y):
    tmp = y - (a * x + b)
    tmp = tmp ** 2  # Square every element in the matrix
    SSE = sum(tmp) / len(x)  # Take the average
    return SSE


# draw all curve point
def draw_hill(x, y):
    a = np.linspace(-20, 20, 100)
    print(a)
    b = np.linspace(-20, 20, 100)
    x = np.array(x)
    y = np.array(y)

    allSSE = np.zeros(shape=(len(a), len(b)))
    for ai in range(0, len(a)):
        for bi in range(0, len(b)):
            a0 = a[ai]
            b0 = b[bi]
            SSE = calc_loss(a=a0, b=b0, x=x, y=y)
            allSSE[ai][bi] = SSE

    a, b = np.meshgrid(a, b)

    return [a, b, allSSE]


#  create simulated data
x = [30, 35, 37, 59, 70, 76, 88, 100]
y = [1100, 1423, 1377, 1800, 2304, 2588, 3495, 4839]

# Data normalization
x_max = max(x)
x_min = min(x)
y_max = max(y)
y_min = min(y)

for i in range(0, len(x)):
    x[i] = (x[i] - x_min) / (x_max - x_min)
    y[i] = (y[i] - y_min) / (y_max - y_min)

plt.plot(x, y, '*r')
# plt.pause(2)

[ha, hb, hallSSE] = draw_hill(x, y)

# init a,b value
a = 10.0
b = -20.0
fig = plt.figure(1, figsize=(12, 8))

# draw fig.1 contour line
plt.subplot(1, 2, 1)
plt.contourf(ha, hb, hallSSE, 15, alpha=0.5, cmap=plt.cm.hot)
C = plt.contour(ha, hb, hallSSE, 15, colors='red')
plt.clabel(C, inline=True)
plt.title('BGD')
plt.xlabel('opt param: a')
plt.ylabel('opt param: b')

plt.ion()  # iteration on

all_loss = []
all_step = []
last_a = a
last_b = b

for step in range(1, 100):
    loss = 0
    all_da = 0
    all_db = 0
    for i in range(0, len(x)):
        y_p = a * x[i] + b
        loss = loss + (y[i] - y_p) * (y[i] - y_p) / 2
        all_da = all_da + da(y[i], y_p, x[i])
        all_db = all_db + db(y[i], y_p)
    loss = loss / len(x)

    # draw fig.1 contour line
    plt.subplot(1, 2, 1)
    plt.scatter(a, b, s=5, color='black')
    plt.plot([last_a, a], [last_b, b], color='blue')

    # draw fig.2 loss line
    all_loss.append(loss)
    all_step.append(step)
    plt.subplot(1, 2, 2)
    plt.plot(all_step, all_loss, color='orange')
    plt.title('BGD')
    plt.xlabel("step")
    plt.ylabel("loss")

    # update param
    last_a = a
    last_b = b
    a = a - rate * all_da
    b = b - rate * all_db

    if step % 5 == 0:
        print("step: ", step, " loss: ", loss, " a: ", a, " b: ", b)
        plt.show()
        plt.pause(0.01)

plt.show()
plt.pause(1000)
