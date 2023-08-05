with open("cc.he.300.vec", encoding="utf-8") as f:
    for ix, w in enumerate(f):
        # print(ix, w)
        # if ix == 1:
        #     break
        if w.split(" ")[0] == "פריז":
            print(w)
        if w.split(" ")[0] == "צרפת":
            print(w)
        if w.split(" ")[0] == "לונדון":
            print(w)
        if w.split(" ")[0] == "אנגליה":
            print(w)
        if w.split(" ")[0] == "בריטניה":
            print(w)