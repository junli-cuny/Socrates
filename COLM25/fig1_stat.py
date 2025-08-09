import numpy as np
from scipy import stats
import re # For parsing the data

def parse_data_string(data_str):
    """Parses a string of space-separated numbers, ignoring 0s."""
    # Use regex to find sequences of digits, optionally with a decimal point
    numbers_str = re.findall(r"[0-9.]+", data_str)
    # Convert to float and filter out zeros
    numbers = [float(n) for n in numbers_str if float(n) != 0.0]
    print(numbers)
    return np.array(numbers) if numbers else np.array([]) # Return empty array if no valid numbers

def calculate_cohens_d(group1, group2):
    """Calculates Cohen's d for independent samples."""
    if len(group1) < 2 or len(group2) < 2: # Need at least 2 samples for variance
        return np.nan
    # Calculate the pooled standard deviation
    n1, n2 = len(group1), len(group2)
    var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1) # Sample variance
    pooled_std = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    if pooled_std == 0: # Avoid division by zero if all values in one group are identical
        return np.nan
    mean_diff = np.mean(group1) - np.mean(group2)
    d = mean_diff / pooled_std
    return d

def get_confidence_interval_diff(group1, group2, alpha=0.05):
    """
    Calculates the confidence interval for the difference between two independent means.
    Assumes unequal variances (Welch's t-test approach for CI).
    """
    if len(group1) < 2 or len(group2) < 2:
        return (np.nan, np.nan)

    mean1, mean2 = np.mean(group1), np.mean(group2)
    var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
    n1, n2 = len(group1), len(group2)

    if n1 == 0 or n2 == 0 or (var1 == 0 and n1 <= 1) or (var2 == 0 and n2 <= 1) : # Avoid division by zero
        return (np.nan, np.nan)

    # Welch-Satterthwaite degrees of freedom
    term1 = var1 / n1
    term2 = var2 / n2
    if term1 == 0 and term2 == 0: # Both variances are zero, e.g., single identical values
        if mean1 == mean2:
            return (0.0, 0.0)
        else:
            return (np.nan, np.nan) # Undefined if means differ but variance is zero

    df_numerator = (term1 + term2)**2
    df_denominator = (term1**2 / (n1 - 1) if n1 > 1 else np.inf) + \
                     (term2**2 / (n2 - 1) if n2 > 1 else np.inf)

    if df_denominator == 0: # Happens if n1=1 and n2=1
        return (np.nan, np.nan)

    df = df_numerator / df_denominator

    if df <= 0: # Should not happen with valid inputs
        return (np.nan, np.nan)

    diff_mean = mean1 - mean2
    se_diff = np.sqrt(term1 + term2)

    t_critical = stats.t.ppf(1 - alpha / 2, df)
    margin_of_error = t_critical * se_diff

    lower_bound = diff_mean - margin_of_error
    upper_bound = diff_mean + margin_of_error
    return (lower_bound, upper_bound)


# --- Paste your data here ---
data_raw_text = {
    "Before": {
        "Assignment 1": """
0	0.960784314	1	0.901960784	0.941176471	0.843137255	0	0.784313725	0.901960784	0.941176471	0.882352941	0.921568627	0.784313725	0.745098039	0.803921569	0	0.764705882	0.764705882	0.882352941	0.862745098	0.68627451	0.823529412	0.941176471	0.941176471	0.941176471	0.784313725	0.980392157	0.843137255	0.921568627	0.901960784	0.607843137	0	0.901960784	1	0.901960784	0.901960784	0.705882353	0.941176471	0.921568627	0.941176471	0.568627451	0.980392157	0.901960784	0.764705882	0.68627451	0.745098039	0.941176471	0.980392157	0.745098039	0	0.784313725	0	0.68627451	0.549019608	0.62745098	0	0.843137255	0.431372549	0.941176471	0.980392157	0.62745098	0.725490196	0.450980392	0.921568627	0.705882353	0.843137255	0.803921569	0.882352941	0	0.764705882	0.784313725	0.745098039	0	0.941176471	0.705882353	0.62745098	0.862745098	0.725490196	0.862745098	0.843137255	0.882352941	0.607843137	0.509803922	0.725490196	0.921568627	0.68627451	0.725490196	0.941176471	1	0	0.862745098	0	0.941176471	0.62745098	0.764705882	0.784313725	0.509803922	0.843137255	0.921568627	0	0.764705882	0.666666667	1	0.941176471	0.666666667	1	0.921568627	0.62745098	0.509803922	0.882352941	1	0.941176471	0.843137255	0.647058824	0	0.823529412	0.901960784	0.882352941	0	0.901960784	1	1	0.37254902	0	0.921568627	0.882352941	0	1	1	0	0	0.882352941	0	0	0.941176471	0	0	0.843137255	0	0	0.843137255	0	0	0.941176471	0	0	0.843137255	0	0	0.803921569	0	0	0.901960784	0	0	0.843137255	0	0	0.941176471	0	0	0.901960784	0	0	0.725490196	0	0	1
        """,
        "Assignment 3": """
0	0	0.78	0.84	0.8	0.76	0	0.72	1	0.96	0.84	0	0.14	0.82	0.72	0	0.84	0.84	0.84	0.84	0.96	0.82	0.82	1	0.82	0.74	1	0.88	0.76	0.94	0.94	0	1	0.78	0.78	0.94	0.74	0.92	1	0.94	0.52	0.92	0.98	0.82	0.98	0.82	0.74	1	0	0	0.78	0	0.78	0.8	0.72	0	0.98	0.82	0.9	0	0.92	0.92	0.8	0	0	0.8	0.88	0	0	0	0.52	0.62	0	0.94	0.86	0	1	0.62	0.7	0.78	1	0.88	0.82	0.72	0	0.94	0	0	0.96	0	0.76	0	1	0	0.68	0.7	0.76	0.7	1	0.6	0.8	0	0.36	0.54	0.28	0.76	0.86	0.98	0.66	0.82	1	0.92	0.82	0.72	0	0.74	0.94	0	0	0.86	1	0.96	0.74	0	0.72	1	0	1	1	0	0	0.76	0	0	0	0	0	1	0	0	0.9	0	0	0.72	0	0	0.82	0	0	0.92	0	0	1	0	0	1	0	0	1	0	0	0.78	0	0	1	0	0	1
        """,
        "Project 1": """
0	0.4	0.875	0.88	0.8875	0.9125	0	0.375	0.8375	0.815	0.7125	0.9	0	0.75	0.8125	0	0.85	0.95	0.85	0.6625	0.95	0.33	0.9375	0.875	1	0.9375	0.9875	0.75	0.75	0.325	0.65	0.2625	0.7875	0.75	0.9625	0.9375	0.71	1	0.875	0.97	0.475	0.9375	1	0.9375	0.95	0.97	1	0.9125	0	0	0.7875	0	0.6875	0.825	0.59	0	0.95	0.79	0.8125	0.85	0.72	0.9	0.85	0	0.875	0.875	0.95	0	0	0	0.8375	0.85	0	0.725	0.8375	0	0.8625	0.85	0.94	0.8375	0.8875	0.97	0.9375	0	0	0.9375	0	0	0.9	0	0.59	0	0.9375	0.3	0.85	0.95	0.69	0.8125	0.9375	0.35	0.7	0	0.7	0.8875	0	0.85	0.125	0.9	0.915	0.125	0.9	0.935	0.6	0.95	0	0.875	1	0.7	0	0.8875	1	0.8125	0	0	0.6625	0.825	0	1	1	0	0	0.75	0	0	0.4625	0	0	0.9375	0	0	0.875	0	0	0.925	0	0	0.8625	0	0	0.9375	0	0	0.9375	0	0	1	0	0	0.9375	0	0	0.4875	0	0	0.9375	0	0	1
        """,
        "Project 2": """
0	0.886363636	0.59	0.931818182	0.977272727	0.6	0	0.886363636	0.64	0.806818182	0.909090909	0.6	0.363636364	0.886363636	0.61	0	0.795454545	0.7	0.977272727	0.931818182	0.63	0.863636364	0.886363636	0.7	0.897727273	0.818181818	0.53	1	0.931818182	0.62	0.568181818	0.386363636	0.68	1	0.886363636	0.71	0.977272727	0.886363636	0.6	1	0.693181818	0.6	0.977272727	0.795454545	0.71	0.965909091	0.886363636	0.7	0	0	0.71	0	0	0.57	0.727272727	0	0.63	0.590909091	0.886363636	0.69	0.738636364	0.886363636	0.71	0	0.704545455	0.7	0.727272727	0.886363636	0	0	1	0.43	0	0.909090909	0.69	0	0.909090909	0.51	0.909090909	0.727272727	0.65	0.840909091	0.931818182	0.62	0	0.931818182	0.34	0	0.875	0.63	0.772727273	0	0.73	0.840909091	0.886363636	0.59	0.795454545	0.886363636	0.71	0.386363636	0.75	0.55	1	0.909090909	0.69	0.852272727	0.886363636	0.59	0.897727273	0.886363636	0.65	0.977272727	0.954545455	0.61	0	0.840909091	0.69	0.931818182	0	0.7	1	0.863636364	0.78	0	0.659090909	0.65	0	1	0.79	0	0	0.65	0	0	0.45	0	0	0.62	0	0	0.63	0	0	0.63	0	0	0.64	0	0	0.82	0	0	0.69	0	0	0.73	0	0	0.64	0	0	0.69	0	0	0.75	0	0	1
        """,
        "Exams": """
0	0.714285714	0.714285714	0.813333333	0.928571429	0.571428571	0	0.828571429	0.728571429	0.92	0.285714286	0.642857143	0.4	0.785714286	0.742857143	0	0.7	0.5	0.84	1	0.857142857	0.586666667	0.828571429	0.857142857	0.893333333	0.828571429	0.828571429	0.893333333	0.714285714	0.828571429	0.693333333	0.8	0.785714286	0.786666667	0.842857143	0.928571429	0.64	0.885714286	0.642857143	0.893333333	0.628571429	0.9	0.893333333	0.857142857	0.928571429	0.84	0.771428571	0.9	0.346666667	0.485714286	0.642857143	0.6	0.714285714	0.857142857	0.453333333	0.2	0.785714286	0.586666667	0.757142857	0.785714286	0.653333333	0.757142857	0.542857143	0	0.571428571	0.535714286	0.786666667	0.685714286	0	0.6	0.585714286	0.928571429	0.466666667	0.857142857	0.642857143	0.106666667	1	0.357142857	0.48	0.9	0.785714286	0.506666667	0.728571429	0.714285714	0.533333333	0.914285714	0.542857143	0.68	0.828571429	0.371428571	0.68	0	0.714285714	0.626666667	0.714285714	0.785714286	0.68	0.514285714	0.642857143	0.36	0.914285714	0.357142857	0.706666667	0.785714286	0.714285714	0.746666667	0.928571429	0.785714286	0.626666667	0.857142857	0.928571429	0.813333333	0.557142857	0.928571429	0.52	0.771428571	0.628571429	0.666666667	0	0.742857143	1	0.857142857	0.457142857	0	0.685714286	0.857142857	0	1	1	0	0	0.857142857	0	0	0.528571429	0	0	0.421428571	0	0	0.75	0	0	0.714285714	0	0	0.614285714	0	0	1	0	0	0.528571429	0	0	0.714285714	0	0	0.8	0	0	0.614285714	0	0	0.614285714	0	0	1
        """
    },
    "After": {
        "Assignment 1": """
0.958169935 0 0.803921569 0.761437908 0 0 0.911764706 0.580392157 0.903921569 0.931372549 0 0.852941176 0 0.902614379 0 0.884313725 0.785620915 0.669281046 0.784313725 0.824183006 0.873856209 0.901960784 0.81372549 0.767973856 0.892810457 0.59869281 1 0 0 0.843137255 0 0.97254902 0 0.911764706 0 0.747058824 0 0.803921569 0.952287582 0.775163399 1 0.804575163 0.805228758 0.883660131 0.815686275 0 0 0.907843137 0.805228758 1 0 0 0 0 0 0
        """,
        "Assignment 3": """
0.88	0	0.81	0	0	0	0.86	0	0	0.94	0	0.84	0	0.98	0	0.52	0	0.86	0.92	0.88	0.92	0.92	0	0	0.84	0.8	0.97	0.86	0	1	0.92	0.94	0.72	0.96	0	0.96	0	0.98	0.88	0.74	0	0.97	0	0.98	0.89	0	0	0.82	0	1	0	0	0	0	0	0
        """,
        "Project 1": """
0.97	0.23	1	0.94	0.11	1	1	0.8	1	1	0	1	0	1	1	0.71	0.82	0.85	1	1	1	1	0.06	0	0.25	0.47	1	1	0	1	0.92	1	0.75	0.99	0	0.97	0	1	0.9	0.84	1	0.94	0.27	0.97	0.89	0	0	0.86	0.86	1	0	0	0	0	0	0
        """,
        "Project 2": """
1	0.7143	0.9365	0	0.3651	1	0.9365	0	0.8413	1	1	0	1	1	0.254	0.5079	0.7143	1	1	1	1	0	0	0	1	1	1	0	1	0.9683	1	0.7778	0.3651	0	1	1	1	0.9048	0.8095	1	0.873	0	0.9365	0.4286	0	0.873	0.746	1	0	0	0	0	0	0	0	0
        """,
        "Exams": """
0.6	0.685714286	0.6	0.780952381	0.738095238	0.857142857	1	0.7	0.7	0.771428571	0.280952381	0.757142857	0	0.628571429	0.657142857	0.671428571	0.542857143	0.452380952	0.928571429	0.780952381	0.871428571	0.914285714	0.857142857	0.128571429	0.785714286	0.39047619	1	0.876190476	0.428571429	0.866666667	0.785714286	0.79047619	0.585714286	0.542857143	0.857142857	0.728571429	0.442857143	1	0.914285714	0.6	0.828571429	0.942857143	0.8	0.647619048	0.642857143	0	0.828571429	0.757142857	0.880952381	0.719756839	1	0	0	0	0	0
        """
    }
}

# --- Process data ---
processed_data = {"Before": {}, "After": {}}
for period in data_raw_text:
    for category, text_data in data_raw_text[period].items():
        parsed_scores = parse_data_string(text_data)
        processed_data[period][category] = parsed_scores * 100


# --- Combine Assignments and Projects as in fig1.py ---
# Categories for output: Assignments_Combined, Projects_Combined, Exams
final_categories = ['Assignments', 'Projects', 'Exams']
output_data = {"Before": {}, "After": {}}

for period in processed_data:
    # Assignments
    as1 = processed_data[period].get("Assignment 1", np.array([]))
    as3 = processed_data[period].get("Assignment 3", np.array([]))
    if as1.size > 0 or as3.size > 0:
      output_data[period]['Assignments'] = np.concatenate((as1, as3))
    else:
      output_data[period]['Assignments'] = np.array([])


    # Projects
    p1 = processed_data[period].get("Project 1", np.array([]))
    p2 = processed_data[period].get("Project 2", np.array([]))
    if p1.size > 0 or p2.size > 0:
      output_data[period]['Projects'] = np.concatenate((p1, p2))
    else:
      output_data[period]['Projects'] = np.array([])

    # Exams
    output_data[period]['Exams'] = processed_data[period].get("Exams", np.array([]))


# --- Calculate and Print Stats ---
print("--- Descriptive Statistics and Significance Tests ---")
print("Note: Scores are 0-100.\n")

means_before_for_fig1 = []
sds_before_for_fig1 = []
means_after_for_fig1 = []
sds_after_for_fig1 = []
p_values_for_fig1 = []


for cat in final_categories:
    print(f"\n--- Category: {cat} ---")
    data_b = output_data["Before"].get(cat, np.array([]))
    data_a = output_data["After"].get(cat, np.array([]))

    if data_b.size < 2: # Need at least 2 data points for std and t-test
        print("  Before: Not enough data")
        mean_b, std_b = np.nan, np.nan
    else:
        mean_b = np.mean(data_b)
        std_b = np.std(data_b, ddof=1) # Sample standard deviation
        print(f"  Before: N={len(data_b)}, Mean={mean_b:.2f}, SD={std_b:.2f}")
    means_before_for_fig1.append(mean_b)
    sds_before_for_fig1.append(std_b)

    if data_a.size < 2:
        print("  After:  Not enough data")
        mean_a, std_a = np.nan, np.nan
    else:
        mean_a = np.mean(data_a)
        std_a = np.std(data_a, ddof=1)
        print(f"  After:  N={len(data_a)}, Mean={mean_a:.2f}, SD={std_a:.2f}")
    means_after_for_fig1.append(mean_a)
    sds_after_for_fig1.append(std_a)


    if data_b.size >= 2 and data_a.size >= 2:
        # Independent t-test (Welch's t-test by default if equal_var=False)
        t_stat, p_value = stats.ttest_ind(data_b, data_a, equal_var=False, nan_policy='omit')
        print(f"  Significance (After vs Before):")
        print(f"    Independent t-test: t-statistic={t_stat:.3f}, p-value={p_value:.4f}")
        if p_value < 0.001: stars = "***"
        elif p_value < 0.01: stars = "**"
        elif p_value < 0.05: stars = "*"
        else: stars = "(ns)"
        print(f"    Significance Level: {stars}")

        # Cohen's d
        d = calculate_cohens_d(data_a, data_b) # Effect of 'After' compared to 'Before'
        print(f"    Cohen's d (Effect Size for After - Before): {d:.3f}")

        # Confidence Interval for the difference in means (Mean_After - Mean_Before)
        ci_lower, ci_upper = get_confidence_interval_diff(data_a, data_b)
        print(f"    95% CI for (Mean_After - Mean_Before): [{ci_lower:.2f}, {ci_upper:.2f}]")
        p_values_for_fig1.append(p_value)
    else:
        print("  Significance: Not enough data for t-test.")
        p_values_for_fig1.append(np.nan)

print("\n\n--- For fig1.py ---")
print(f"categories = {final_categories}") # Use this for labels
print(f"means_before = {means_before_for_fig1}")
print(f"sds_before = {sds_before_for_fig1}")
print(f"means_after = {means_after_for_fig1}")
print(f"sds_after = {sds_after_for_fig1}")
print(f"p_values_for_stars = {p_values_for_fig1} # Use these p-values for significance stars in fig1.py")
