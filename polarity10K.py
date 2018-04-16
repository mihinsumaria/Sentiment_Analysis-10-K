from SECEdgar import download_all_10_K
from polarity import plot_all_polarities
import nltk

nltk.download('words')
download_all_10_K()
plot_all_polarities()