from django.conf import settings
class AlgorithmCode:
    def startAlgo(self):
        import pandas as pd
        import matplotlib.pyplot as plt

        # importing the dataset
        columns = ['buying_price', 'maintainence_cost', 'number_of_doors', 'number_of_seats', 'luggage_boot_size',
                   'safety_rating']
        train = settings.MEDIA_ROOT + "\\" + "train.csv"
        test = settings.MEDIA_ROOT + "\\" + "test.csv"
        prediction = settings.MEDIA_ROOT + "\\" + "prediction.csv"
        train = pd.read_csv(train)
        test = pd.read_csv(test, names=columns)

        # columns=['buying_price','maintainence_cost','number_of_doors','number_of_seats','luggage_boot_size','safety_rating']

        # fitting the model
        from sklearn import svm
        X = train[columns]
        y = train.popularity
        clf = svm.SVC(kernel="rbf", C=300)
        clf = clf.fit(X, y)
        pred = clf.predict(test[columns])

        # preparing the csv file
        submission_df = {"0": pred}
        submission = pd.DataFrame(submission_df)
        m = submission.to_csv(prediction, index=False, header=False)
        # print('pred',pred)
