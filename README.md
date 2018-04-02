# KNN
k-nearest neighbors algorithm

### KNN Introduction:

```
最近鄰居法（KNN演算法，又譯K-近鄰演算法）是一種用於分類和回歸的無母數統計方法，KNN常用來做資料分類。
KNN是一種監督式學習(Supervised learning)，監督式學習需透過資料訓練出一個model，但KNN沒有做training的動作。
K為使用者自己定義的常數，KNN就是選擇離自己最近的K的鄰居(Data)，之後觀察哪一種類別(Tag)的鄰居最多就將自己也當成該類別。
```
### Input:

```
1.使用Ettoday新聞作為訓練集分類。
2.使用jieba作為分詞，取出top 100 word 作為每篇文章的關鍵詞。
3.取出k=3個最近鄰居作為分類依據，此外對最近的第一個鄰居作為加權*2
```

### Output:

![image](https://github.com/Larix/KNN/blob/master/1.jpg)
