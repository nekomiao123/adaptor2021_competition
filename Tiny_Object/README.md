# 小目标检测

## 医学小目标检测

参考链接 https://zhuanlan.zhihu.com/p/138108192

### 使用“滑窗”，变小为大，检测变分类

查找了近两年来，这个方向发表的论文。意外发现，大家在总体思路上，几乎都采用了相同的套路。概括起来，就是使用“滑窗”抠图方法，每次只“抠出”一个很小的区域进行分析，在这个很小的区域中，“小”目标也就变成了“大”目标，而检测问题也变成了在这个小区域内是否包含病变的“二分类”问题。对一幅尺寸不大的图像，进行二分类判断，简直是深度学习网络最拿手的入门问题啊。

#### 基础思想

用sliding window滑动出很多小的patches 然后把这些小patches送入CNN

这篇论文先把每一幅尺寸为512x512的眼底彩照进行降采样，缩小到256x256；然后，采用尺寸为16x16窗口从最左上角开始滑动，一共可以得到224x224=50716个尺寸为16x16的Patches。这里，因为限制窗口不能超出图像，所以最终Patches数目比256x256要少。

接下来，就是把每一个16x16的Patch作为单独的图像，输入一个8层的CNN网络，进行二分类预测。关于这个8层CNN，不专门说了，是一个非常标准（常规）的CNN。

需要说的是，对每一个Patch，进行二分类（有/无 Hard Exudate）后，实际决定的是这个Patch的中心像素，所对应的原始图像中的像素，是被分割为病灶（前景），还是非病灶（背景）。

#### 改造

- 改CNN，改为resnet-50连接SVM进行分类
- 增加数据预处理，使用了两种方法，第一种是“Illumination Equalization, and Contrast Enhancement”，第二种是“ Top-hat transformation”。第一种效果好

#### 进阶

本篇论文的创新点之一，就是先使用传统图像处理方法（高斯混合模型），对图像进行整体分析（特征增强），快速定位出疑似病灶的区域，然后只在疑似区域范围内生成Patches，再用CNN对生成的Patches进行分类。

作为另外一个创新点，在分类器的设计上，作者不仅使用了更复杂的深度网络，而且是把当前三个最流行的深度学习分类网络都纳入囊中，组合起来使用。这三个网络分别是Inception-v3，RestNet-50，VGG-19。

### 优化的Faster R-CNN

首先，对于常规Faster R-CNN容易漏掉小目标的问题，作者对Faster R-CNN进行了改进。包括两个方面：1）根据要检测的目标大小，修改重新设置了RPN阶段的Anchors尺寸，从而更好的定位小目标；2）选择FPN的不同层级网络，把高分辨率Feature Map和低分辨率Feature Map级联，从而在最终的Feature Map中包含小目标信息。

![img](https://pic2.zhimg.com/80/v2-a08adad9acab2e3744f8c0a9ff95ee9d_1440w.jpg)

其次，在常规Proposal Region以外，额外增加了包含范围更大的Context Region，用于帮助识别是否包含目标。作者提到，有时目标太小了，在Feature Map中变成了一个像素，很难判断是背景还是目标。因此，作者创造性引入了Context Region，来解决这个问题。大家看下图，应该就可以理解。

![img](https://pic2.zhimg.com/80/v2-309a07748ca71186c2b3f1d34b1954e1_1440w.jpg)

此外，为了解决缺少阳性样本，样本极度不均衡问题，作者采用了两种处理方法。1）对阳性样本引入随机旋转，达到样本扩容；2）在每个Batch抽样选择样本时，允许对阳性样本重复选择，多次利用，从而达到样本均衡。



# 某评论

\1. Patch的方法感觉大同小异：如何有效的取到patch，用更深的网络和boosting来提高分类效果，其实创新有限。 且受限fixed patch size和特征 一般网络都是设计成2分类来解决单一lesion的检测 



\2. 用弱监督实现检测我觉得是值得探索的方向： 比如pixel-level的标注数据是比较珍贵的，而image-level的分类标签是比较充分的（譬如来自kaggle, messidor etc 5类图像标签）， 如何利用这些标签来实现pixel-level的detection，现在也有类似工作



\3. 据我所知，目前为止是没有detection方法（yolo, retinalNet，faster-rcnn, ssd）在fundus上的应用，主要原因是没有类似的标注集(血管分割有STARE DRIVE, lesion mask也有 DB1, e-ophtha等 但是没有类似voc, coco的眼底库)。我尝试用过一个small dataset来训练yolo_v3， 效果不够好，除了size这个问题外，遥感相比fundus的检测感觉还是有很大不同的。