# kNN(k-nearest neighbors algorithm)
此專案以新聞分類進行kNN範例之實作

### kNN Introduction:

```
最近鄰居法（KNN演算法，又譯K-近鄰演算法）是一種用於分類和回歸的無母數統計方法，KNN常用來做資料分類。
KNN是一種監督式學習(Supervised Learning)，監督式學習需透過資料訓練出一個model，但KNN沒有做training的動作。
K為使用者自己定義的常數，KNN就是選擇離自己最近的K的鄰居(Data)，之後觀察哪一種類別(Tag)的鄰居最多就將自己也當成該類別。
```
### Input:

測試文章 : [台股遇長假前賣壓 失守10900點](https://tw.news.yahoo.com/%E5%8F%B0%E8%82%A1%E9%81%87%E9%95%B7%E5%81%87%E5%89%8D%E8%B3%A3%E5%A3%93-%E5%A4%B1%E5%AE%8810900%E9%BB%9E-062006790.html)  
```
1.使用ETtoday新聞作為訓練集分類。
2.使用Jieba作為分詞，取出Top 100 Words 作為每篇文章的關鍵詞。
3.取出k=3個最近鄰居作為分類依據，此外對最近的第一個鄰居作為加權*2
```

### Output:

![image](https://github.com/Larix/KNN/blob/master/1.jpg)
