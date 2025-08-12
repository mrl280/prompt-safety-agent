# TD-IDF Classifier

In order to train a simple regression model, raw text was converted to number feature vectors by means of TF-IDF, which were then used as inputs for model training.

Term frequency (TF) is a measure of how often a single term appears in a single document. In this study, TF is a measure of how often a specific token appears in an prompt. TF is calucated as:

$$
\mathrm{TF}(t, p) = \frac{f_{t,p}}{\sum_{k} f_{k,p}}
\tag{1}
$$

where  \(f_{t,p}\) is the number of times token \(t\) appears in prompt \(p\) and \(\sum_{k} f_{k,p}\) is the total number of token in the database.

Inverse document frequency (IDF) is a measure of the rarity of a specific term across a corpus of documents. In this study, IDF is a measure of how often a specific word appears in the dataset. IDF is calculated as:

$$
\mathrm{IDF}(t) = \log \frac{N}{1 + n_t}
\tag{2}
$$

where \(N\) is the total number of prompts in the database and \(n_t\) is the number of prompts that contain the token \(t\).

TF does not capture the overall importance of a token across the entire dataset, and IDF does not take into account the frequency of a term within individual examples. Therefore, combining them as TF-IDF balances both local and global token importance for better comprehension.

TF-IDF (Term Frequency-Inverse Document Frequency) is a statistic measure of the relevant importance of a word in an example relative to a collection of examples.
