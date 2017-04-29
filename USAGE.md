# Usage
1. 在mid文件夹下存放原始的midi音乐
2. `cd tool-chain`，依次执行`mid2xml.sh`, `sequentialize2.sh`(`sequentialize.sh`也可以，但推荐后者), `xml2pkl.sh`, `merge.sh`
3. `cd ..; cp data.pkl CompoNet/data/train.pkl`
4. `cd CompoNet`
5. 训练的模型会保存到`save`，如果想重新训练，请保证`save`是空的
6. `./train.py`
7. 训练过程中按ctrl+c会出现输入指令的提示，c为继续，q为退出，w为保存训练模型，l为修改学习速率（未实现……）
8. 训练结束后，`./sample.py`生成乐曲，前奏为训练数据的前x个note
9. `cd ../output; ./output2xml.py; xml2mid.py`，生成`output.mid`

# 调参指南
可调的参数在下面几个位置：
* `compo_net.py`中Config类的定义(建议在train.py中传给Config的参数里改）
* `compo_net.py`中_sample函数决定取样方法
* `sample.py`中初始序列长度
