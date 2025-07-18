import os
import analisador as an
URL = os.getcwd()
print(URL)

if __name__ == '__main__':
    an.analisar(os.path.join(URL, 'auth.log'))
    ...