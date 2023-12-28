def Entry_Fee(row):
    if row['kata']=='Yes' and row['kumite']=='No':
        return 1000
    elif row['kumite']=='Yes' and row['kata']=='No':
        return 1000
    else:
        return 1500


