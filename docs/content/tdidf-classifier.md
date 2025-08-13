# TD-IDF Classifier

Based on dataset exploration, n-grams, particularly unigrams, provide a strong signal for distinguishing between safe and unsafe prompts. Leveraging this insight, a logistic regression model was trained on the TF-IDF vectorized representations of the prompts.

TF-IDF (Term Frequency-Inverse Document Frequency) is a statistic measure of the relevant importance of a word in an example relative to a collection of examples. Term frequency (TF) is a measure of how often a single term appears in a single document. TF is calculated as:

\[
\mathrm{TF}(t, p) = \frac{f_{t,p}}{\sum_{k} f_{k,p}}
\tag{2}
\]

where  \(f_{t,p}\) is the number of times term \(t\) appears in prompt \(p\) and \(\sum_{k} f_{k,p}\) is the total number of terms in the database. Inverse document frequency (IDF) is a measure of the rarity of a specific term across a corpus of documents. IDF is calculated as:

\[
\mathrm{IDF}(t) = \log \frac{N}{1 + n_t}
\tag{3}
\]

where \(N\) is the total number of prompts in the database and \(n_t\) is the number of prompts that contain the term \(t\).

Because TF does not capture the overall importance of a term across the dataset, and IDF does not account for the frequency of a term within individual examples, combining them as TF-IDF balances term relevance within each example, improving model comprehension. Raw text was transformed into numerical feature vectors using TF-IDF, which were then used as inputs for model training.

A initial text classification model was trained using vanilla TF-IDF vectorization combined with a vanilla logistic regression classifier. This was implemented using the following [scikit-learn](https://scikit-learn.org/stable/) pipeline:

```python
clf = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("logreg", LogisticRegression())
])
```

Common evaluation metrics for the test set are provided in Table 1, while metrics for the training set are summarized in Table 2. These reports include precision, recall, F1-score, and support for each class, as well as overall accuracy, macro average, and weighted average.

<p align="center"><strong>Table 1:</strong> Train Set Performance Metrics for Vanilla Classifier</p>

<table>
  <thead>
    <tr>
      <th>Class</th>
      <th>Precision</th>
      <th>Recall</th>
      <th>F1-Score</th>
      <th>Support</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Safe (0)</td>
      <td>0.9827</td>
      <td>0.9991</td>
      <td>0.9908</td>
      <td>5740</td>
    </tr>
    <tr>
      <td>Unsafe (1)</td>
      <td>0.9979</td>
      <td>0.9595</td>
      <td>0.9783</td>
      <td>2496</td>
    </tr>
    <tr>
      <td>accuracy</td>
      <td></td>
      <td></td>
      <td>0.9871</td>
      <td>8236</td>
    </tr>
    <tr>
      <td>macro avg</td>
      <td>0.9903</td>
      <td>0.9793</td>
      <td>0.9846</td>
      <td>8236</td>
    </tr>
    <tr>
      <td>weighted avg</td>
      <td>0.9873</td>
      <td>0.9871</td>
      <td>0.9871</td>
      <td>8236</td>
    </tr>
  </tbody>
</table>

<br>

<p align="center"><strong>Table 2:</strong> Test Set Performance Metrics for Vanilla Classifier</p>

<table>
  <thead>
    <tr>
      <th>Class</th>
      <th>Precision</th>
      <th>Recall</th>
      <th>F1-Score</th>
      <th>Support</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Safe (0)</td>
      <td>0.9744</td>
      <td>0.9993</td>
      <td>0.9867</td>
      <td>1410</td>
    </tr>
    <tr>
      <td>Unsafe (1)</td>
      <td>0.9984</td>
      <td>0.9431</td>
      <td>0.9699</td>
      <td>650</td>
    </tr>
    <tr>
      <td>accuracy</td>
      <td></td>
      <td></td>
      <td>0.9816</td>
      <td>2060</td>
    </tr>
    <tr>
      <td>macro avg</td>
      <td>0.9864</td>
      <td>0.9712</td>
      <td>0.9783</td>
      <td>2060</td>
    </tr>
    <tr>
      <td>weighted avg</td>
      <td>0.9820</td>
      <td>0.9816</td>
      <td>0.9814</td>
      <td>2060</td>
    </tr>
  </tbody>
</table>

<br>

Immediately, the model demonstrates strong performance, with both training and test accuracy exceeding 98%. The similarity between the metrics reported in Tables 1 and 2 no strong evidence of overfitting. For safe prompts, recall is nearly perfect (99.93%) and precision is high (97.44%), showing that almost all safe prompts were correctly identified. For unsafe prompts, precision is extremely high (99.84%), but recall is lower (94.31%), indicating that a notable portion of unsafe prompts were missed.

Figure 5 presents the confusion matrix for this classifier evaluated on the test set.

{{ plot:conf_matrix_test_vanilla.html }}

<p align="center"><strong>Figure 5:</strong> Test Set Confusion Matrix for Vanilla Classifier. Misclassified positives (unsafe prompts predicted as safe) are shown the bottom-left corner and misclassified negatives (safe prompts predicted as unsafe) are shown in the top-right corner.</p>

For safety-critical applications, recall for unsafe prompts should be prioritized, even at the expense of some precision. In this case, the model misclassified only one safe prompt as unsafe, but 37 unsafe prompts were labeled as safe, which is unacceptable for a production system. This discrepancy indicates that, although overall accuracy is high, the model requires adjustment to reduce the risk of misclassified unsafe prompts.

## Weight tuning

Dataset exploration revealed a class imbalance: approximately 70% of examples are safe prompts, while only 30% are unsafe. This imbalance is also seen in the _support_ column in Table 1 and Table 2, where the safe class has substantially higher counts than the unsafe class. To mitigate the effects of the 70/30 class distribution, class weights were adjusted based on the inverse of their respective frequencies (i.e., using a balanced weighting scheme).

Table 3 presents the evaluation metrics for the model with balanced weights on the test set, and Figure 6 shows the corresponding confusion matrix.

<p align="center"><strong>Table 3:</strong> Test Set Performance Metrics Using Balanced Weights</p>

<table>
  <thead>
    <tr>
      <th>Class</th>
      <th>Precision</th>
      <th>Recall</th>
      <th>F1-Score</th>
      <th>Support</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Safe (0)</td>
      <td>0.9853</td>
      <td>0.9972</td>
      <td>0.9912</td>
      <td>1410</td>
    </tr>
    <tr>
      <td>Unsafe (1)</td>
      <td>0.9937</td>
      <td>0.9677</td>
      <td>0.9805</td>
      <td>650</td>
    </tr>
    <tr>
      <td>accuracy</td>
      <td></td>
      <td></td>
      <td>0.9879</td>
      <td>2060</td>
    </tr>
    <tr>
      <td>macro avg</td>
      <td>0.9895</td>
      <td>0.9824</td>
      <td>0.9859</td>
      <td>2060</td>
    </tr>
    <tr>
      <td>weighted avg</td>
      <td>0.9879</td>
      <td>0.9879</td>
      <td>0.9878</td>
      <td>2060</td>
    </tr>
  </tbody>
</table>

{{ plot:conf_matrix_test_balanced_weights.html }}

<p align="center"><strong>Figure 6:</strong> Test Set Confusion Matrix for Balanced Weights</p>

As shown in Table 3 and Figure 6, balancing the class weights improved the model, increasing test set recall for unsafe prompts from 94.31% to 96.77%. The confusion matrix indicates that misclassified positives decreased from 37 to 21, while misclassified negatives increased slightly from 1 to 4.

Because the correct identification of unsafe prompts is critical, custom class weights were explored to disproportionately favor the unsafe class. Experiments indicated that a weight ratio of `1:5` yielded the best results. Further emphasizing unsafe prompts during training fails to further increase the recall, and precision and overall accuracy begin to meaningfully decline.

Table 4 presents the evaluation metrics for the model with custom weights on the test set, and Figure 7 shows the corresponding confusion matrix.

<p align="center"><strong>Table 4:</strong> Test Set Performance Metrics Using Custom Weights</p>

<table>
  <thead>
    <tr>
      <th>Class</th>
      <th>Precision</th>
      <th>Recall</th>
      <th>F1-Score</th>
      <th>Support</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Safe (0)</td>
      <td>0.9936</td>
      <td>0.9950</td>
      <td>0.9943</td>
      <td>1410</td>
    </tr>
    <tr>
      <td>Unsafe (1)</td>
      <td>0.9892</td>
      <td>0.9862</td>
      <td>0.9877</td>
      <td>650</td>
    </tr>
    <tr>
      <td>accuracy</td>
      <td></td>
      <td></td>
      <td>0.9922</td>
      <td>2060</td>
    </tr>
    <tr>
      <td>macro avg</td>
      <td>0.9914</td>
      <td>0.9906</td>
      <td>0.9910</td>
      <td>2060</td>
    </tr>
    <tr>
      <td>weighted avg</td>
      <td>0.9922</td>
      <td>0.9922</td>
      <td>0.9922</td>
      <td>2060</td>
    </tr>
  </tbody>
</table>

{{ plot:conf_matrix_test_custom_weights.html }}

<p align="center"><strong>Figure 7:</strong> Test Set Confusion Matrix for Custom Weights</p>

As shown in Table 5 and Figure 7, this weighting increases recall for unsafe prompts to 98.62% and raises overall test set accuracy above 99%. The confusion matrix indicates that missed unsafe prompts were further reduced to 9, while misclassified negatives further increased to 7.

## Adding bigrams and trigrams

Based on dataset exploration, unigrams provided the strongest signal, while bigrams and trigrams were expected to further improve class separation. Consequently, bigrams and trigrams were incorporated into the TF-IDF features for model training. Table 5 and Figure 8 show the test set evaluation metrics and the corresponding confusion matrix for the model with custom weights and \( n \)-gram features.

<p align="center"><strong>Table 5:</strong> Test Set Performance Metrics Using Custom Class Weights with Bigrams and Trigrams</p>

<table>
  <thead>
    <tr>
      <th>Class</th>
      <th>Precision</th>
      <th>Recall</th>
      <th>F1-Score</th>
      <th>Support</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Safe (0)</td>
      <td>0.9957</td>
      <td>0.9943</td>
      <td>0.9950</td>
      <td>1410</td>
    </tr>
    <tr>
      <td>Unsafe (1)</td>
      <td>0.9877</td>
      <td>0.9908</td>
      <td>0.9892</td>
      <td>650</td>
    </tr>
    <tr>
      <td>accuracy</td>
      <td></td>
      <td></td>
      <td>0.9932</td>
      <td>2060</td>
    </tr>
    <tr>
      <td>macro avg</td>
      <td>0.9917</td>
      <td>0.9925</td>
      <td>0.9921</td>
      <td>2060</td>
    </tr>
    <tr>
      <td>weighted avg</td>
      <td>0.9932</td>
      <td>0.9932</td>
      <td>0.9932</td>
      <td>2060</td>
    </tr>
  </tbody>
</table>

{{ plot:conf_matrix_test_final.html }}

<p align="center"><strong>Figure 8:</strong> Test Set Confusion Matrix for Custom Weights with Bigrams and Trigrams</p>

Including n-grams of lengths 1, 2, and 3 provides a slight improvement in model performance, raising the recall for unsafe prompts above 99%. The confusion matrix shows that misclassified positives decrease from 9 to 6, while misclassified negatives increase slightly from 7 to 8. Consequently, this is the best-performing iteration of this model, and it serves as the TD-IDF classifier in the production system.

## Confidence analysis

Up to this point, predictions have been obtained using [`predict()`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html#sklearn.linear_model.LogisticRegression.predict), which returns the predicted class labels. Alternatively, [`predict_proba()`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html#sklearn.linear_model.LogisticRegression.predict_proba) can be used to return predicted class probabilities, providing a quantitative measure of the model’s confidence in each prediction.

Figure 9 presents the distribution of prediction confidences produced by the TF-IDF classifier. This analysis examines the model’s certainty across predicted classes and assesses whether misclassifications are concentrated at lower confidence levels.

{{ plot:tdidf_confidence_distribution.html }}

<p align="center"><strong>Figure 9:</strong> Distribution of prediction confidences separated by predicted class and classification correctness. Each boxplot shows the range and density of confidence scores for correct and incorrect predictions within each predicted class. Misclassified points are shown in red.</p>

Figure 4 shows that misclassifications do tend to occur at lower confidence levels, particularly for false positives (safe prompts incorrectly predicted as unsafe). However, false negatives (unsafe prompts predicted as safe) remain a concern, as the model’s confidence for these errors can be as high as 85%.
