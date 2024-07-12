import attacks.bit_flipping_attack
from nn_scheme.NCorrFP_scheme import NCorrFP


def test_knn():
#    scheme = CategoricalNeighbourhood(gamma=1)
    scheme = NCorrFP(gamma=1, fingerprint_bit_length=16)
    data = "datasets/breast_cancer_full.csv"
    fingerprinted_data = scheme.insertion('breast-cancer', primary_key='Id', secret_key=601, recipient_id=4,
                                          outfile='nn_scheme/outfiles/fp_data_blind_corr_all_attributes.csv',
                                          correlated_attributes=['age', 'menopause', 'inv-nodes', 'node-caps'])
#
#    suspect = scheme.detection(fingerprinted_data, secret_key=100, original_data=data)
    #print(fingerprinted_data)
    #columns = ['Id'] + list(fingerprinted_data.columns)
    #fingerprinted_data['Id'] = fingerprinted_data.index
    #fingerprinted_data = fingerprinted_data[columns]
    #print(fingerprinted_data)

    suspect = scheme.detection(fingerprinted_data, secret_key=601, primary_key='Id',
                               correlated_attributes=['age', 'menopause', 'inv-nodes', 'node-caps'],
                               original_columns=["age","menopause","tumor-size","inv-nodes","node-caps","deg-malig","breast","breast-quad",
    "irradiat","recurrence"])


def knn_adult_census():
    scheme = NCorrFP(gamma=10, fingerprint_bit_length=32)

    fingerprinted_data = scheme.insertion('adult', primary_key='Id', secret_key=100, recipient_id=4,
                                          outfile='nn_scheme/outfiles/adult_fp_acc_wc_en_100.csv',
                                          correlated_attributes=['relationship', 'marital-status', 'occupation', 'workclass', 'education-num'])
    suspect = scheme.detection(fingerprinted_data, secret_key=100, primary_key='Id',
                               correlated_attributes=['relationship', 'marital-status', 'occupation', 'workclass',
                                                      'education-num'])


def test_vertical_attack_bc():
    scheme = NCorrFP(gamma=1, fingerprint_bit_length=8)
    fingerprinted_data = scheme.insertion('breast-cancer', primary_key='Id', secret_key=601, recipient_id=4,
                                          outfile='nn_scheme/outfiles/fp_data_blind_corr_all_attributes.csv',
                                          correlated_attributes=['age', 'menopause', 'inv-nodes', 'node-caps'])
    fingerprinted_data = fingerprinted_data.drop(['age'], axis=1)
    suspect = scheme.detection(fingerprinted_data, secret_key=601, primary_key='Id',
                               correlated_attributes=['age', 'menopause', 'inv-nodes', 'node-caps'],
                               original_columns=["age", "menopause", "tumor-size", "inv-nodes", "node-caps",
                                                 "deg-malig", "breast", "breast-quad",
                                                 "irradiat", "recurrence"])


def test_vertical_adult():
    scheme = NCorrFP(gamma=20, fingerprint_bit_length=32)

    fingerprinted_data = scheme.insertion('adult', primary_key='Id', secret_key=100, recipient_id=4,
                                          outfile='nn_scheme/outfiles/adult_fp_acc_wc_en_100.csv',
                                          correlated_attributes=['relationship', 'marital-status', 'occupation',
                                                                 'workclass', 'education-num'])
    fingerprinted_data = fingerprinted_data[["Id", "age", "workclass","fnlwgt","education","education-num",
                                                 "marital-status","occupation"]]
    suspect = scheme.detection(fingerprinted_data, secret_key=100, primary_key='Id',
                               correlated_attributes=['relationship', 'marital-status', 'occupation', 'workclass',
                                                      'education-num'],
                               original_columns=["age","workclass","fnlwgt","education","education-num",
                                                 "marital-status","occupation",
                                                 "relationship","race","sex","capital-gain","capital-loss",
                                                 "hours-per-week","native-country","income"])


def test_flipping_bc():
    scheme = NCorrFP(gamma=1, fingerprint_bit_length=16)

    fingerprinted_data = scheme.insertion('breast-cancer', primary_key='Id', secret_key=100, recipient_id=4,
                                          outfile='nn_scheme/outfiles/adult_fp_acc_wc_en_100.csv',
                                          correlated_attributes=['age', 'menopause', 'inv-nodes', 'node-caps'])
    attack = attacks.bit_flipping_attack.BitFlippingAttack()
    attacked_data = attack.run(fingerprinted_data, 0.01)
    print(attacked_data.size)
    scheme.detection(attacked_data, secret_key=100, primary_key='Id',
                     correlated_attributes=['age', 'menopause', 'inv-nodes', 'node-caps'])


def test_flipping_adult():
    scheme = NCorrFP(gamma=1, fingerprint_bit_length=16)

    fingerprinted_data = scheme.insertion('adult', primary_key='Id', secret_key=100, recipient_id=4,
                                          outfile='nn_scheme/outfiles/adult_fp_acc_wc_en_100.csv',
                                          correlated_attributes=['relationship', 'marital-status', 'occupation',
                                                                 'workclass', 'education-num'])
    attack = attacks.bit_flipping_attack.BitFlippingAttack()
    attacked_data = attack.run(fingerprinted_data, 0.01)
    scheme.detection(fingerprinted_data, secret_key=100, primary_key='Id',
                     correlated_attributes=['relationship', 'marital-status', 'occupation', 'workclass',
                                            'education-num'])


def test_demo():
    scheme = NCorrFP(gamma=1, fingerprint_bit_length=16)
    data = "datasets/breast_cancer_full.csv"
    fingerprinted_data, iter_log = scheme.demo_insertion('breast-cancer', primary_key='Id', secret_key=601, recipient_id=4,
                                          outfile='nn_scheme/outfiles/fp_data_blind_corr_all_attributes.csv',
                                          correlated_attributes=['age', 'menopause', 'inv-nodes', 'node-caps'])
    #
    suspect, d_iter_log = scheme.demo_detection(fingerprinted_data, secret_key=601, primary_key='Id',
                               correlated_attributes=['age', 'menopause', 'inv-nodes', 'node-caps'],
                               original_columns=["age", "menopause", "tumor-size", "inv-nodes", "node-caps",
                                                 "deg-malig", "breast", "breast-quad",
                                                 "irradiat", "recurrence"])
    return d_iter_log


if __name__ == '__main__':
    test_knn()
