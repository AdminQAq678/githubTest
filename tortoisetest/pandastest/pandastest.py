import pandas as pd
print(pd.__version__)

mydataset = {
    'sites': ["Google", "Runoob", "Wiki"],
    'number': [1, 2, 3]
}

myvar = pd.DataFrame(mydataset)
serial = pd.Series(mydataset['number'], index=(
    'asdsd', 'sdfdsf', 'sdfdf'), name='my serail')


data = [['Google', 10], ['Runoob', 12], ['Wiki', 13]]

df = pd.DataFrame(data, columns=['Site', 'Age'], dtype=float)


if __name__ == '__main__':
    print(serial)
    print(myvar)
    print(df)
