import tensorflow as tf
import numpy as np
from tensorflow.keras.layers import Layer,Embedding,Bidirectional,LSTM,Input,Dot,Reshape,Lambda,Dense,Dropout

#from tensorflow.keras import Sequential

class hyper_params:
    '''
    num_dup应该少取，正例的个数通过epoch堆上去
    num_neg应该适当，也是通过epoch堆上去，过大损失函数会平滑掉，过小后期很难产生新的负例
    epoch很多时，每个正例对应的选择过负例次数增加，从而使得正例对其它负例的分值大于20
    对于相似问题，更应该让它出现在负例中，从而在预测时有明显的差距，后续应该在构造数据集时手动去构造
    
    '''
    def __init__(self):
        #batch_size如果和num_dup一样就会在一个batch中的正例完全一样

        self.epoch=10000
        
        self.optlist=['adam','adagrad','sgd','rmsprop']
        self.optimizer=self.optlist[0]
        self.learning_rate=0.01
        self.batch_size=62#实际是62*4=248

        #以下是
        #正例尽量多取，一个正例对应的负例不要太多
        #如果考虑推送多个相似问题的话，负例就不能完全随机
        #需要定义相似问题不能作为负例选取
        
        #两个都选1的效果好
        self.num_dup=1
        self.num_neg=1
        
        self.embed_units=256
        self.num_units=128
        self.vocab_size=266#包括pad和unk
        self.top_k=8#不要选的太大，有可能在交互时得到的矩阵元素个数不够
        self.dropout=0.3
        self.num_mlp_layer=2
        self.mlp_num_units=16
        self.mlp_activation='relu'#'sigmoid'
        
        self.mlp_num_fan_out=5
        #输出维度是5,在最后的输出之前先降下维度？

        self.remove_checkpoint=False
        self.bilinear = False

class MVLSTM(tf.keras.Model):
    def __init__(self, hyper_params, *args, **kwargs):
        super(MVLSTM,self).__init__(*args,**kwargs)
        self.hp = hyper_params
        self.embedding = Embedding(self.hp.vocab_size,self.hp.embed_units,mask_zero = True)

        self.bilstm1 = Bidirectional(LSTM(self.hp.num_units,return_sequences=True,dropout=self.hp.dropout))
        self.bilstm2 = Bidirectional(LSTM(self.hp.num_units,return_sequences=True,dropout=self.hp.dropout))

        self.mlp_layer = [Dense(self.hp.mlp_num_units,activation=self.hp.mlp_activation) for _ in range(self.hp.num_mlp_layer)]
        self.mlp_layer.append(Dense(self.hp.mlp_num_fan_out,activation=self.hp.mlp_activation))
        
        self.dropout = Dropout(rate=self.hp.dropout)

        #预测模型，采用hinge_loss,也可以考虑分类模型
        self.dense = Dense(1,activation='linear')
        
    def build(self,input_shape):
        
        if self.hp.bilinear:
            print("采用bilinear模式")
            self.bilinear = self.add_weight(name = "bilinear weight",shape = (self.hp.embed_units,self.hp.embed_units),initializer = 'glorot_uniform',trainable = True)
        
        super(MVLSTM,self).build(input_shape)
        
    def call(self,inputs):
        """inputs:[left,right],left:[batch_size,T1],right:[batch_size,T2]"""
        
        #inputs作为列表输入
        left,right=inputs[0],inputs[1]
        
        left = self.embedding(left)
        right = self.embedding(right)
        
        left = self.bilstm1(left)#[batch_size,T1,embed_size]
        right = self.bilstm2(right)#[batch_size,T2,embed_size]
        
        match_matrix = Dot(axes=[2,2],normalize = False)([left,right])

        #在除了batch_size维度上进行flatten
        matching_signals = Reshape((-1,))(match_matrix)

        #取topk,有可能不够，要保证T1*T2 >= topk
        matching_topk = Lambda(lambda x: tf.math.top_k(x, k=self.hp.top_k, sorted=True)[0])(matching_signals)
        #维度为[batch_size,top_k]
        
        #多层感知机的激活函数为relu
        mlp = matching_topk
        for layer in self.mlp_layer:
            mlp = layer(mlp)
        
        #mlp=self.mlp_layer(matching_topk)
        
        #添加dropout,注意call的参数training=None，默认在非训练时不实现dropout效果
        #if training:
            
        mlp = self.dropout(mlp)
        
        #这里不用分类
        output=self.dense(mlp)
        output=tf.squeeze(output)
        
        return output

def test_mvlstm():
    
    hp = hyper_params()
    print(hp.batch_size)
    
    my_model = MVLSTM(hp)
    inputs=[Input((20,),hp.batch_size),Input((22,),hp.batch_size)]

    a = tf.convert_to_tensor(np.random.randint(0,10,(32,4)))
    b = tf.convert_to_tensor(np.random.randint(0,10,(32,19)))

    print(a.dtype)
    #inputs=[a,b]

    ans = my_model(inputs)
    print(ans.shape)
    return ans

if __name__ == "__main__":

    ans = test_mvlstm()
