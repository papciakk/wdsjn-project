import pickle
import numpy as np

with open("result.pickle", "rb") as f:
    x = pickle.load(f)

text = x['text']

text_np = np.array(text, dtype=np.int32)
del text

with open("text.pickle", "wb") as f:
    pickle.dump(text_np, f)

del text_np

with open("dict.pickle", "wb") as f:
    pickle.dump(x['dict'], f)

del x['dict']

with open("rdict.pickle", "wb") as f:
    pickle.dump(x['rev_dict'], f)

del x['rev_dict']

del x