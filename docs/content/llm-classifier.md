# LLM Classifier

As LLM technology has advanced, smaller and more efficient models capable of running on consumer-grade hardware have emerged, making LLMs more accessible to a wider range of users.

<p align="center"><strong>Table 9:</strong> Test Set Performance Metrics for Qwen3-4B-Instruct-2507</p>

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
      <td>0.90</td>
      <td>0.99</td>
      <td>0.94</td>
      <td>1404</td>
    </tr>
    <tr>
      <td>Unsafe (1)</td>
      <td>0.96</td>
      <td>0.77</td>
      <td>0.86</td>
      <td>649</td>
    </tr>
    <tr>
      <td>accuracy</td>
      <td></td>
      <td></td>
      <td>0.92</td>
      <td>2053</td>
    </tr>
    <tr>
      <td>macro avg</td>
      <td>0.93</td>
      <td>0.88</td>
      <td>0.90</td>
      <td>2053</td>
    </tr>
    <tr>
      <td>weighted avg</td>
      <td>0.92</td>
      <td>0.92</td>
      <td>0.92</td>
      <td>2053</td>
    </tr>
  </tbody>
</table>

Figure 10 shows ...

{{ plot:conf_matrix_lmm_test_Qwen3-4B-Instruct-2507.html }}

<p align="center"><strong>Figure 10:</strong> Test Set Confusion Matrix for Qwen3-4B-Instruct-2507</p>

<p align="center"><strong>Table 10:</strong> Test Set Performance Metrics for Mistral-7B-Instruct-v0.3</p>

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
      <td>0.93</td>
      <td>0.92</td>
      <td>0.92</td>
      <td>1336</td>
    </tr>
    <tr>
      <td>Unsafe (1)</td>
      <td>0.82</td>
      <td>0.85</td>
      <td>0.83</td>
      <td>601</td>
    </tr>
    <tr>
      <td>accuracy</td>
      <td></td>
      <td></td>
      <td>0.90</td>
      <td>1937</td>
    </tr>
    <tr>
      <td>macro avg</td>
      <td>0.88</td>
      <td>0.88</td>
      <td>0.88</td>
      <td>1937</td>
    </tr>
    <tr>
      <td>weighted avg</td>
      <td>0.90</td>
      <td>0.90</td>
      <td>0.90</td>
      <td>1937</td>
    </tr>
  </tbody>
</table>

<p align="center"><strong>Figure 11:</strong> Test Set Confusion Matrix for Mistral-7B-Instruct-v0.3</p>

{{ plot:conf_matrix_lmm_test_Mistral-7B-Instruct-v0.3.html }}
