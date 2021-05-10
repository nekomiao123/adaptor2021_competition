# Medical_competition
## adaptor2021

用来记录比赛的思路和阅读的一些论文

比赛地址 https://adaptor2021.github.io

比赛要求 检测二尖瓣修复手术时候的线穿入和穿出的点

额外要求 使用GAN把模拟手术场景变换成真实手术场景 [参考论文](https://arxiv.org/abs/1806.03627)

## 对比赛的理解

首先，比赛的名字全称为Deep Generative Model Challenge for Domain Adaptation in Surgery，我们从中可窥探，他跟生成模型和领域自适应关系密切。

从比赛的简述中，我们得知他就是想利用模拟的手术去适应真实的手术情况（因为隐私保护的缘故），所以他提供了很多的模拟手术数据集，而相对来说真实情况的数据集就小很多了。这就是为了用GAN去减小模拟手术和真实手术中的差别（这里有两篇相关文献[1](https://arxiv.org/abs/1806.03627) [2](https://arxiv.org/abs/1906.10011)）。

比赛的目的是从target domain（这是领域自适应的概念）中去标记landmarks。这些landmarks就是缝线在心脏组织上的入点和出点。只会在真实手术的场景中对模型进行评估，因此只在真实场景中提出landmark的检测方案是可能有效的。更复杂的方法就是结合两个领域的数据，然后在入点出点或者特征上去调整。

另外就是这个比赛要去比较不同的image2image的方法将模拟数据转化成真实数据的效果，这个过程中要改变模拟场景但是不能改变手术线或者手术器材之类的东西。尽管这种转换只能用肉眼去评估，但还是假设缝线在两种场景下的一致性作为参考的标准。

鼓励使用image2image的方法去转换，但不是强制的。

任务：

- 只在手术数据集上训练一个landmark的检测方法
- 使用模拟数据集当做预训练的模型（做数据融合）
- 通过使用更先进的输入、输出、特征级领域适应方法的组合来整合仿真领域，可能采用端到端训练策略
- 其他



比赛规则

- 方法是全自动的
- 不能用预训练的模型或者用其他的数据集
- 一个队伍只能注册一次，所有提交都是一个账号
- 一名参赛者只能参加一个队伍
- 在docker提交之后，参赛队伍必须写LNCS论文描述使用的具体方法。不交论文视为成绩无效。
- 前三发证书，没赞助商惨兮兮



关于数据集

缝线是蓝色和白色的。

故意把真实数据集搞得很小来强迫选手结合模拟数据集和真实数据集



关于提交

- 必要：模型可以根据图片输出一个json文件，文件里面就是标记
- 可选：模型可以做一个image2image的转换，把模拟数据集转换为真实数据集。

关于阶段

训练期、平台测试期、测试期

训练期：自己拿training dateset训练

平台测试期：主要测试数据格式 官方修bug

测试期：参赛者总共能交三次，取最好的作为结果。docker运行在24GB的泰坦显卡上，需要注意不能超过泰坦的内存（谁有这钱买得起泰坦啊）

![image-20210418210327520](https://cdn.jsdelivr.net/gh/nekomiao123/pic/img/image-20210418210327520.png)



模型评估

**true positives**, **false positives** and **false negatives**

- true positive    if it lies within a radius of 6 pixels around the manually labeled point, same as in [[4](https://adaptor2021.github.io/#4)]. 
- Finally, we report **sensitivity/recall** (TPR) and **precision** (PPV).

排名

用F-score或者F1-score作为排名，越高越好。

### 目前思路

~~使用小目标检测来做~~

https://github.com/kuanhungchen/awesome-tiny-object-detection

小目标的思路估摸着不对，应该用特征点检测来做

就是landmark detection



### 有用的网址

MICCAI2021 https://www.miccai2021.org/en/

MICCAI2020 https://www.miccai2020.org/en/MICCAI-2020-CHALLENGES.html

MICCAI2020比赛讲解 https://zhuanlan.zhihu.com/p/119949534

老师给的比赛网址 https://grand-challenge.org/challenges/

paperwithcode https://paperswithcode.com/search?q_meta=&q_type=&q=medical

一个介绍 https://www.rsipvision.com/ComputerVisionNews-2021May/20/

