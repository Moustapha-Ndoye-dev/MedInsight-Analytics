import pandas as pd

def analyser_groupes(df, groupby_col, target_col, agg_func='mean'):
    """Agrégation pour comprendre les statistiques (par département, maladie, etc.)."""
    return df.groupby(groupby_col)[target_col].agg(agg_func).reset_index().sort_values(target_col, ascending=False)
