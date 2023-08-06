import pandas as pd
import pingouin as pg
from scipy.stats import pearsonr


def cronbach_alpha_scale_if_deleted(df):
    gca = pg.cronbach_alpha(df)
    result = pd.DataFrame(columns=["Item", "Scale Mean if Item Deleted", "Scale Variance if Item Deleted",
                                   "Corrected Item-Total Correlation", "Cronbach's Alpha if Item Deleted"])
    for column in df:
        sub_df = df.drop([column], axis=1)
        ac = pg.cronbach_alpha(sub_df)
        scale_mean = sub_df.mean().sum()
        variance = sub_df.sum(axis=1).var()
        pr = pearsonr(sub_df.mean(axis=1), df[column])
        result = result.append({'Item': column, "Scale Mean if Item Deleted": scale_mean, "Scale Variance if Item Deleted": variance,
                                "Corrected Item-Total Correlation": pr[0], "Cronbach's Alpha if Item Deleted": ac[0]}, ignore_index=True)
    return [gca, result]
