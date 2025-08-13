# TD-IDF Classifier

In order to train a simple regression model, raw text was converted to number feature vectors by means of TF-IDF, which were then used as inputs for model training.

Term frequency (TF) is a measure of how often a single term appears in a single document. In this study, TF is a measure of how often a specific token appears in an prompt. TF is calculated as:

\[
\mathrm{TF}(t, p) = \frac{f_{t,p}}{\sum_{k} f_{k,p}}
\tag{2}
\]

where  \(f_{t,p}\) is the number of times token \(t\) appears in prompt \(p\) and \(\sum_{k} f_{k,p}\) is the total number of token in the database.

Inverse document frequency (IDF) is a measure of the rarity of a specific term across a corpus of documents. In this study, IDF is a measure of how often a specific word appears in the dataset. IDF is calculated as:

\[
\mathrm{IDF}(t) = \log \frac{N}{1 + n_t}
\tag{3}
\]

where \(N\) is the total number of prompts in the database and \(n_t\) is the number of prompts that contain the token \(t\).

TF does not capture the overall importance of a token across the entire dataset, and IDF does not take into account the frequency of a term within individual examples. Therefore, combining them as TF-IDF balances both local and global token importance for better comprehension.

TF-IDF (Term Frequency-Inverse Document Frequency) is a statistic measure of the relevant importance of a word in an example relative to a collection of examples.

## Vanilla classifier

A text classification model was trained using vanilla TF-IDF vectorization combined with a vanilla logistic regression classifier. This was implemented using the following [scikit-learn](https://scikit-learn.org/stable/) pipeline:

```python
clf = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("logreg", LogisticRegression())
])
```

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

Figure 5 shows ...

{{ plot:conf_matrix_test_vanilla.html }}

<p align="center"><strong>Figure 5:</strong> Test Set Confusion Matrix for Vanilla Classifier</p>

TODO: Add analysis

## Weight tuning

Dataset exploration revealed a class imbalance: approximately 70% of examples are safe prompts, while only 30% are unsafe. This imbalance is reflected in the _support_ column in Table 1 and Table 2. To mitigate the effects of this 70/30 class distribution, class weights were adjusted to be inversely proportional to their respective frequencies.

<p align="center"><strong>Table 3:</strong> Train Set Performance Metrics Using Balanced Weights</p>

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
      <td>0.9931</td>
      <td>0.9972</td>
      <td>0.9951</td>
      <td>5740</td>
    </tr>
    <tr>
      <td>Unsafe (1)</td>
      <td>0.9935</td>
      <td>0.9840</td>
      <td>0.9887</td>
      <td>2496</td>
    </tr>
    <tr>
      <td>accuracy</td>
      <td></td>
      <td></td>
      <td>0.9932</td>
      <td>8236</td>
    </tr>
    <tr>
      <td>macro avg</td>
      <td>0.9933</td>
      <td>0.9906</td>
      <td>0.9919</td>
      <td>8236</td>
    </tr>
    <tr>
      <td>weighted avg</td>
      <td>0.9932</td>
      <td>0.9932</td>
      <td>0.9932</td>
      <td>8236</td>
    </tr>
  </tbody>
</table>

<p align="center"><strong>Table 4:</strong> Test Set Performance Metrics Using Balanced Weights</p>

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

Figure 6 shows ...

{{ plot:conf_matrix_test_balanced_weights.html }}

<p align="center"><strong>Figure 6:</strong> Test Set Confusion Matrix for Balanced Weights</p>

Tables 3 and 4 show that giving fair importance to all classes leads to a more robust and accurate model. Next, custom weighting strategies were explored to further improve recall. A weighting ratio of about `1:5` is the maximum before recall stops improving and precision and accuracy begin to decline.

<p align="center"><strong>Table 5:</strong> Train Set Performance Metrics Using Custom Weights</p>

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
      <td>0.9997</td>
      <td>0.9962</td>
      <td>0.9979</td>
      <td>5740</td>
    </tr>
    <tr>
      <td>Unsafe (1)</td>
      <td>0.9913</td>
      <td>0.9992</td>
      <td>0.9952</td>
      <td>2496</td>
    </tr>
    <tr>
      <td>accuracy</td>
      <td></td>
      <td></td>
      <td>0.9971</td>
      <td>8236</td>
    </tr>
    <tr>
      <td>macro avg</td>
      <td>0.9955</td>
      <td>0.9977</td>
      <td>0.9966</td>
      <td>8236</td>
    </tr>
    <tr>
      <td>weighted avg</td>
      <td>0.9971</td>
      <td>0.9971</td>
      <td>0.9971</td>
      <td>8236</td>
    </tr>
  </tbody>
</table>

<p align="center"><strong>Table 6:</strong> Test Set Performance Metrics Using Custom Weights</p>

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

Figure 7 shows ...

{{ plot:conf_matrix_test_custom_weights.html }}

<p align="center"><strong>Figure 7:</strong> Test Set Confusion Matrix for Custom Weights</p>

## Adding bigrams and trigrams

Based on our dataset exploration, bigrams and trigrams may aid class separation.

<p align="center"><strong>Table 7:</strong> Train Set Performance Metrics Using Custom Class Weights with Bigrams and Trigrams</p>

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
      <td>0.9998</td>
      <td>0.9991</td>
      <td>0.9995</td>
      <td>5740</td>
    </tr>
    <tr>
      <td>Unsafe (1)</td>
      <td>0.9980</td>
      <td>0.9996</td>
      <td>0.9988</td>
      <td>2496</td>
    </tr>
    <tr>
      <td>accuracy</td>
      <td></td>
      <td></td>
      <td>0.9993</td>
      <td>8236</td>
    </tr>
    <tr>
      <td>macro avg</td>
      <td>0.9989</td>
      <td>0.9994</td>
      <td>0.9991</td>
      <td>8236</td>
    </tr>
    <tr>
      <td>weighted avg</td>
      <td>0.9993</td>
      <td>0.9993</td>
      <td>0.9993</td>
      <td>8236</td>
    </tr>
  </tbody>
</table>

<p align="center"><strong>Table 8:</strong> Test Set Performance Metrics Using Custom Class Weights with Bigrams and Trigrams</p>

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

Figure 8 shows ...

{{ plot:conf_matrix_test_final.html }}

<p align="center"><strong>Figure 8:</strong> Test Set Confusion Matrix for Custom Weights with Bigrams and Trigrams</p>

## Confidence analysis

Figure 9 shows ...

{{ plot:tdidf_confidence_distribution.html }}

<p align="center"><strong>Figure 9:</strong> Distribution of prediction confidences separated by predicted class and classification correctness. Each boxplot visualizes the range and density of confidence scores for correct and incorrect predictions within each predicted class. Misclassified points are shown in red.</p>
