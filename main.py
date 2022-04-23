FILENAME = "example.fss"


def read_fss(fss):
    data_array = []
    with open(fss) as data:
        for line in data:
            if not line.startswith((">", "\n")):
                if line.endswith("None\n"):
                    data_array.append(line[:-5])
                elif line.endswith("\n"):
                    data_array.append(line[:-1])
                else:
                    data_array.append(line)
    return data_array


def save_fss(fss, name):
    fss_text = ""
    file = open("{}_normalized.fss".format(name[:-4]), "w")
    for i in fss:
        i = i.replace("k", "K")
        i = i.replace("s", "S")
        fss_text += i + "\n"
    file.write(fss_text)
    file.close()


def normalize_fss(data_array):
    pre_raw_data_array = []
    for idx, x in enumerate(data_array):
        if ";" in x:
            for y in x.split(";"):
                if y != "":
                    pre_raw_data_array.append(y)
        else:
            pre_raw_data_array.append(x)

    normalized_fss = []
    volume = 'a'
    loop = False
    loop_new_vol = False
    loop_log = []
    for idx, x in enumerate(pre_raw_data_array):
        if idx == 0:
            if not x.startswith("t"):
                normalized_fss.append("t" + x)
            else:
                normalized_fss.append(x.lower())
        elif x.lower().startswith("t") and not loop:
            normalized_fss.append(x.lower())
        elif x.lower().startswith("v"):
            if loop:
                loop_new_vol = True
            volume = x.lower()[1:2]
        elif x.lower().startswith("ls"):
            loop = True
        elif x.lower().startswith("l") and loop:
            loop_count = x[1:2]
            for i in range(int(loop_count)):
                for z in loop_log:
                    if type(z) == list:
                        if z[1][1]:
                            normalized_fss.append(z[0] + z[1][0])
                        else:
                            if i > 0:
                                normalized_fss.append(z[0] + volume)
                            else:
                                normalized_fss.append(z[0] + z[1][0])
                    else:
                        normalized_fss.append(z)
            loop = False
            loop_log = []
            loop_new_vol = False
        else:
            if x.lower().startswith(("r", "k", "s", "t")):
                new_value = x.lower()
            else:
                x_list = list(x)
                if len(x_list) > 3:
                    new_value = x_list[0] + x_list[1] + x_list[2] + x_list[3]
                else:
                    if loop:
                        new_value = [x_list[0] + x_list[1] + x_list[2], [volume, loop_new_vol]]
                    else:
                        new_value = x_list[0] + x_list[1] + x_list[2] + volume

            if loop:
                loop_log.append(new_value)
            else:
                normalized_fss.append(new_value)

    return normalized_fss


# Normalize fSound
data_array = read_fss(FILENAME)
normalized_fss = normalize_fss(data_array)
save_fss(normalized_fss, FILENAME)
