# coding: utf-8
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn import preprocessing
import numba
import time

total_start = time.time()

def get_train_test():
    start = time.time()
    train = pd.read_csv('../train_pca.csv')
    test = pd.read_csv('../test_pca_outcome.csv')
    people_pca = pd.read_csv('../people_pca_char1-9.csv')
    #char_pca = pd.read_csv('char_act_pca_2.csv')
    dummy_pca = pd.read_csv('../dummy_people_pca.csv')
    people_dates = pd.read_csv('../people_dates.csv')
    #binary_sum = pd.read_csv('../binary_sum.csv', usecols=['people_id', 'binary_sum'])
    print 'Done reading csv files'

    people_dates.fillna('0 ', inplace=True)
    people_dates['days_passed'] = people_dates.last_action.apply(lambda x: int(x.split(' ')[0]))

    last_action_day = {}
    for row in people_dates[['people_id', 'date', 'days_passed']].values:
        last_action_day[(row[0], row[1])] = row[2]

    train = pd.merge(train, people_pca, on='people_id', how='left')
    test = pd.merge(test, people_pca, on='people_id', how='left')

    train = pd.merge(train, dummy_pca, on='people_id', how='left')
    test = pd.merge(test, dummy_pca, on='people_id', how='left')

    #train = pd.merge(train, binary_sum, on='people_id', how='left')
    #test = pd.merge(test, binary_sum, on='people_id', how='left')

    #train['binary_sum'] = train.binary_sum.apply(lambda x: int(x, 2))
    #test['binary_sum'] = test.binary_sum.apply(lambda x: int(x, 2))

    print 'Done merging people_pca'
    print 'Total time passed: ', (time.time()-start)
    del people_pca, dummy_pca, people_dates#, binary_sum

    train['char_10_y'] = train['char_10_y'].apply(int)
    test['char_10_y'] = test['char_10_y'].apply(int)
    for i in range(11, 38):
        train['char_{}'.format(i)] = train['char_{}'.format(i)].apply(int)
        test['char_{}'.format(i)] = test['char_{}'.format(i)].apply(int)

    print 'Done converting bool to int'

    @numba.jit
    def get_date(x):
        if x[1] < 10:
            month = '0' + str(x[1])
        else:
            month = str(x[1])
        if x[2] < 10:
            day = '0' + str(x[2])
        else:
            day = str(x[2])
        year = str(x[0])
        return year + '-' + month + '-' + day

    train['date'] = map(get_date, train[['year_x', 'month_x','day_x']].values)
    test['date'] = map(get_date, test[['year_x', 'month_x','day_x']].values)

    outcome = {}
    for row in train[['group_1', 'date', 'outcome']].values:
        outcome[(row[0], row[1])] = row[2]

    def get_outcome(x):
        try:
            return outcome[tuple(x)]
        except:
            return -1

    train['last_action'] = map(lambda x: last_action_day[tuple(x)], train[['people_id', 'date']].values)
    test['last_action'] = map(lambda x: last_action_day[tuple(x)], test[['people_id', 'date']].values)

    train['date_y'] = map(get_date, train[['year_y', 'month_y','day_y']].values)
    test['date_y'] = map(get_date, test[['year_y', 'month_y','day_y']].values)

    #test['outcome'] = map(get_outcome, test[['group_1', 'date']].values)
    #print 'Done getting test outcome'

    train = train.append(test[test.outcome!=-1])
    test = test[test.outcome==-1]

    print 'Done splitting/merging test'

    val_list = ['activity_category', 'char_1_x', 'char_2_x', 'char_3_x', 'char_4_x',
                'char_5_x', 'char_6_x', 'char_7_x', 'char_8_x', 'char_9_x', 'char_10_x']
    char_list = ['char_10_y', 'char_11', 'char_12',
                 'char_13', 'char_14', 'char_15', 'char_16', 'char_17', 'char_18',
                 'char_19', 'char_20', 'char_21', 'char_22', 'char_23', 'char_24',
                 'char_25', 'char_26', 'char_27', 'char_28', 'char_29', 'char_30',
                 'char_31', 'char_32', 'char_33', 'char_34', 'char_35', 'char_36', 'char_37']

    @numba.jit
    def get_char(vals):
        if vals[0] == 1:
            return np.mean(vals[1:9])
        else:
            return vals[10]

    @numba.jit
    def get_true(vals):
        i = 0
        for v in vals:
            if v == True:
                i +=1
        return i

    @numba.jit
    def get_false(vals):
        i = 0
        for v in vals:
            if v == False:
                i += 1
        return i

    @numba.jit
    def get_bool_diff(vals):
        i = 0
        for v in vals:
            if v == True:
                i += 1
            elif v == False:
                i -= 1
        return i

    @numba.jit
    def get_date_diff(d1, d2):
        d = 0
        for i in range(3):
            d += np.abs(d1[i] - d2[i])
        return d

    @numba.jit
    def get_date_num(d):
        d1 = 0
        d[0] = d[0] - 2020
        for i in range(3):
            d1 += d[i]
        return d1

    @numba.jit
    def get_date_rat(d1, d2):
        d1_num = get_date_num(d1)
        d2_num = get_date_num(d2)
        return d1_num/d2_num

    @numba.jit
    def binary_sum(row):
        bsum = 0
        for val in row:
            bsum += val
        return bsum

    print 'Total time passed: ', (time.time()-start)

    train['char_x'] = map(get_char, train[val_list].values)
    test['char_x'] = map(get_char, test[val_list].values)
    train['true_count'] = map(get_true, train[char_list].values)
    train['false_count'] = map(get_false, train[char_list].values)
    test['true_count'] = map(get_true, test[char_list].values)
    test['false_count'] = map(get_false, test[char_list].values)
    train['bool_count'] = map(get_bool_diff, train[char_list].values)
    test['bool_count'] = map(get_bool_diff, test[char_list].values)
    train['binary_sum'] = map(binary_sum, train[['char_10_y'] + ['char_{}'.format(i) for i in range(11, 38)]].values)
    test['binary_sum'] = map(binary_sum, test[['char_10_y'] + ['char_{}'.format(i) for i in range(11, 38)]].values)

    date_mean_y = train.groupby('date_y')['outcome'].mean().to_dict()
    date_mean = train.groupby('date')['outcome'].mean().to_dict()

    date_count_y = train.groupby('date_y')['outcome'].count().to_dict()
    date_count = train.groupby('date')['outcome'].count().to_dict()

    date_mean['2022-01-16'] = 0.
    date_mean_y['2022-01-16'] = 0.
    date_count['2022-01-16'] = 0.
    date_count_y['2022-01-16'] = 0.

    train['date_mean'] = train.date.apply(lambda x: date_mean[x])
    test['date_mean'] = test.date.apply(lambda x: date_mean[x])

    train['date_mean_y'] = train.date_y.apply(lambda x: date_mean_y[x])
    test['date_mean_y'] = test.date_y.apply(lambda x: date_mean_y[x])

    train['date_count'] = train.date.apply(lambda x: date_count[x])
    test['date_count'] = test.date.apply(lambda x: date_count[x])

    train['date_count_y'] = train.date_y.apply(lambda x: date_count_y[x])
    test['date_count_y'] = test.date_y.apply(lambda x: date_count_y[x])

    train['activity_type'] = train.activity_id.apply(lambda x: int(x.split('_')[0][-1]))
    test['activity_type'] = test.activity_id.apply(lambda x: int(x.split('_')[0][-1]))

    print 'Finished getting bool features'

    le = preprocessing.LabelEncoder()
    le.fit(list(train.people_id.unique()) + list(test.people_id.unique()))
    train['people'] = le.transform(train['people_id'])
    test['people'] = le.transform(test['people_id'])

    le2 = preprocessing.LabelEncoder()
    le2.fit(list(train['activity_id'].unique()) + list(test['activity_id'].unique()))
    train['activity'] = le2.transform(train['activity_id'])
    test['activity'] = le2.transform(test['activity_id'])

    #le3 = preprocessing.LabelEncoder()
    #le3.fit(list(train['date'].unique()) + list(test['date'].unique()))
    #train['date'] = le3.transform(train['date'])
    #test['date'] = le3.transform(test['date'])

    le3 = preprocessing.LabelEncoder()
    le3.fit(list(train['date'].unique()) + list(test['date'].unique()))
    train['date_x'] = le3.transform(train['date'])
    test['date_x'] = le3.transform(test['date'])

    le4 = preprocessing.LabelEncoder()
    le4.fit(list(train['date_y'].unique()) + list(test['date_y'].unique()))
    train['date_y'] = le4.transform(train['date_y'])
    test['date_y'] = le4.transform(test['date_y'])

    print 'Finished label encoding'

    print 'Total time passed: ', (time.time()-start)


    train['date_num'] = map(get_date_num, train[['year_x', 'month_x', 'day_x']].values)
    test['date_num'] = map(get_date_num, test[['year_x', 'month_x', 'day_x']].values)


    train['date_diff'] = map(get_date_diff, train[['year_x', 'month_x', 'day_x']].values,
                             train[['year_y', 'month_y', 'day_y']].values)
    test['date_diff'] = map(get_date_diff, test[['year_x', 'month_x', 'day_x']].values,
                            test[['year_y', 'month_y', 'day_y']].values)

    train['date_rat'] = map(get_date_diff, train[['year_x', 'month_x', 'day_x']].values,
                             train[['year_y', 'month_y', 'day_y']].values)
    test['date_rat'] = map(get_date_diff, test[['year_x', 'month_x', 'day_x']].values,
                            test[['year_y', 'month_y', 'day_y']].values)

    print 'Finished date features'

    train['char_sum'] = map(sum, train[['char_{}_y'.format(i) for i in range(1,10)]].values)
    test['char_sum'] = map(sum, test[['char_{}_y'.format(i) for i in range(1,10)]].values)

    train['char_pca_sum'] = map(sum, train[['char_pca{}'.format(i) for i in range(10)]].values)
    test['char_pca_sum'] = map(sum, test[['char_pca{}'.format(i) for i in range(10)]].values)

    train['char_38_scaled'] = train['char_38'].apply(lambda x: float(x/100.))
    test['char_38_scaled'] = test['char_38'].apply(lambda x: float(x/100.))

    #char_mean = train.groupby('char_38')['outcome'].mean().to_dict()
    #def get_char_mean(x):
    #    try:
    #        return char_mean[tuple(x)]
    #    except:
    #        return 0.

    #train['char_mean'] = train['char_38'].apply(get_char_mean)
    #test['char_mean'] = test['char_38'].apply(get_char_mean)

    train.fillna(-999, inplace=True)
    test.fillna(-999, inplace=True)

    print 'Done generating train/test'

    return train, test


def gen_solution(n_est):
    X_all = ['char_pca9',
             'char_x',
             'char_pca2',
             'day_x',
             'date_num',
             'date_diff',
             'date_rat',
             'month_x',
             'char_5_y',
             'char_9_y',
             'bool_count',
             'char_4_y',
             'true_count',
             'char_3_y',
             'binary_sum',
             'false_count',
             'char_8_y',
             'date_x',
             'char_6_y',
             'char_pca0',
             'people',
             'char_7_y',
             'char_2_y',
             'group_1',
             'char_38_scaled'
            ]
    y = 'outcome'

    clf = RandomForestClassifier(n_estimators=n_est, verbose=10, n_jobs=1, random_state=42)#, max_depth=35)

    train, test = get_train_test()

    train.drop([x for x in train.columns if x not in X_all+[y]], axis=1, inplace=True)
    test.drop([x for x in test.columns if x not in X_all+[y, 'activity_id']], axis=1, inplace=True)

    print 'Fitting classifier'
    start = time.time()

    clf.fit(train[X_all], train[y])

    print 'Done in {} seconds'.format(start-time.time())

    del train

    pred = clf.predict_proba(test[X_all])[:,1]
    #pred1 = pred[:,1]

    submission = pd.DataFrame()
    submission['activity_id'] = test['activity_id']
    submission['outcome'] = pred
    del test

    test2 = pd.read_csv('../test_pca_outcome.csv')
    submission = submission.append(test2[test2.outcome!=-1][['activity_id', 'outcome']])
    submission.to_csv('submission-random_forest-n_est{}-outcome.csv'.format(n_est), index=False)

gen_solution(2000)
print 'Finished generating solution'
print 'Total time elapsed: {}'.format(time.time() - total_start)
