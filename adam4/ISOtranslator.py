import textract
import traceback
import re


# ------------------------------------STRING ANALYSIS------------------------------------ #

def analyze_pdf(path , verbose=False):
    print("\u001B[36mAnalyzing document...\u001B[0m" , end='' , flush=True)

    try:
        document_as_bytes = textract.process(path , encoding='utf-8')
        if verbose:
            print("\u001B[32;1mDone. Analysis result:\u001B[0m")
            print(str(document_as_bytes))
        else:
            print("\u001B[32;1mDone.\u001B[0m")
        return document_as_bytes
    except:
        print("\u001B[31;1mError.\u001B[0m")
        traceback.print_exc()


def encode_bytes(bytes , verbose=False):
    print("\u001B[36mEncoding bytes...\u001B[0m" , end='' , flush=True)

    document_as_string = bytes.decode('utf8')
    if verbose:
        print("\u001B[32;1mDone. Retrieved text from bytes:\u001B[0m")
        print(document_as_string)
    else:
        print("\u001B[32;1mDone.\u001B[0m")
    return document_as_string


def rectify_document_as_string(string, verbose=False):
    print("\u001B[36mRectifying string...\u001B[0m" , end='' , flush=True)

    string = string.replace("\t", " ")
    string = re.sub(' +', ' ', string)
    string = string.strip()
    if verbose:
        print("\u001B[32;1mDone. Rectified string:\u001B[0m")
        print(string)
    else:
        print("\u001B[32;1mDone.\u001B[0m")
    return string


# ------------------------------------TEXT ANALYSIS------------------------------------ #

def generate_superhaystack(text , verbose=False):
    print("\u001B[36mGenerating Superhaystack...\u001B[0m" , end='' , flush=True)

    print("\u001B[36mRemoving head and tail...\u001B[0m" , end='' , flush=True)
    head = text.find("Cuando existen normas de producto aplicables, su terminología se utiliza en esta norma internacional") + 128
    tail = text.find("Miembros de ISO 9999 en la familia OMS de clasificaciones internacionales")

    superhaystack = text[head:tail]

    print("\u001B[36mRemoving headers and footers...\u001B[0m", end='', flush=True)
    side = "LICENCIA PARA UN USUARIO. COPIA Y USO EN RED PROHIBIDAS\n\nDIRECCIÓN DE NORMALIZACIÓN DE INTECO AUTORIZA" \
           " ELUSO DE ESTA NORMA PARA LOS MIEMBROS DEL CTN 03/SC 02\n"
    header = "UNE-EN ISO 9999:2017"
    footer = "LICENCIA PARA UN USUARIO. COPIA Y USO EN RED PROHIBIDAS\n\nDIRECCIÓN DE NORMALIZACIÓN DE INTECO " \
             "AUTORIZA EL USO DE ESTA NORMA PARA LOS MIEMBROS DEL CTN 03/SC 02"

    superhaystack = superhaystack.replace(side , "")
    superhaystack = superhaystack.replace(header , "")
    superhaystack = superhaystack.replace(footer , "")

    split_haystack = superhaystack.splitlines(True)
    unsplit_haystack_parts = []
    for line in split_haystack:
        if "véase" not in line:
            unsplit_haystack_parts.append(line)

    superhaystack = "".join(unsplit_haystack_parts)

    print("\u001B[36mRemoving page numbers...\u001B[0m", end='', flush=True)
    superhaystack.replace("", "")
    superhaystack = re.sub('-\s\d{1,3}\s-' , "" , superhaystack)
    superhaystack = re.sub('\n+', "\n\n", superhaystack)

    superhaystack = superhaystack.strip()
    superhaystack = "\n99\n\n" + superhaystack + "\n\n99\n"

    if verbose:
        print("\u001B[32;1mDone. Generated superhsytack:\u001B[0m")
        print(superhaystack)
    else:
        print("\u001B[32;1mDone.\u001B[0m")
    return superhaystack


def clean_string(string , verbose=False):
    string = string.replace("\n", " ")
    string = string.replace("\t", " ")
    string = re.sub(' +', ' ', string)
    string = string.strip()

    print_result("String cleaned", string, verbose)
    return string


def get_next_item(haystack , verbose=False):
    match = re.findall('(?P<code>\n\d{2}\s?\d{0,2}\s?\d{0,2}\n)' , haystack , re.DOTALL)
    start = match[0]
    end = match[1]

    item = haystack[haystack.find(start) : haystack.find(end) + len(end)]

    print_result("Item retreived" , item , verbose)
    return item

def get_next_subclass(haystack, verbose=False):
    # TODO: mejorar esto. hay que usar grupos de expresiones regulares, en vez de tener una dirt_subclass y luego una clean_subclass
    # TODO: este metodo está obsoleto
    match = re.search('\d{2}\s\d{2}\n+.+\n+\d{2}\s\d{2}', haystack)
    dirty_subclass = match.group(0)

    clean_sublass = re.sub('\n+\d{2}\s\d{2}\n*' , '' , dirty_subclass)

    print_result("Subclass retreived", clean_sublass, verbose)
    return clean_sublass


def delete_next_item(haystack, item, verbose=False):
    index = haystack.find(item)
    item = re.sub('\n\d{2}\s?\d{0,2}\s?\d{0,2}\n' , "" , item[::-1] , count=1)[::-1]
    if index != -1:
        haystack = haystack[index + len(item):]

        print_result("Next item deleted. Haystack updated", haystack , verbose)
        return haystack
    else:
        print("\u001B[31mError: couldn't find subclass.\u001B[0m")


def get_class_code_from_subclass(subclass , as_string=False , verbose=False):
    class_code = int(subclass[:2])

    if as_string:
        class_code = str(class_code)

    print_result("Class code retrieved", class_code, verbose)
    return class_code


def get_subclass_code_from_subclass(subclass , as_string=False , verbose=False):
    subclass_code = int(subclass[3:5])

    if as_string:
        subclass_code = str(subclass_code)

    print_result("Subclass code retrieved", subclass_code, verbose)
    return subclass_code


def get_subclass_name_from_subclass(subclass , verbose=False):
    match = re.search('\n+(?P<subclass_name>.+\n*.*)', subclass)
    subclass_name = match.group('subclass_name')

    print_result("Subclass name retrieved" , subclass_name , verbose)

    return subclass_name


def print_result(title , result , verbose):
    if verbose:
        separator_len = 80

        title_len = separator_len - len(title)
        title_padding = int(title_len/2)

        for i in range(title_padding):
            title = "=" + title + "="

        print("\u001B[32;1m"+title+"\u001B[0m")
        print(str(result))
        for i in range(separator_len):
            print("\u001B[32;1m=\u001B[0m" , end="")
        print("")









# ------------------------------------MAIN------------------------------------ #

def main():
    print("\n    _____  _____  ____  _                       _       _             \n   |_   _|/ ____|/ __ \| |                     | |     | |            \n     | | | (___ | |  | | |_ _ __ __ _ _ __  ___| | __ _| |_ ___  _ __ \n     | |  \___ \| |  | | __| '__/ _` | '_ \/ __| |/ _` | __/ _ \| '__|\n    _| |_ ____) | |__| | |_| | | (_| | | | \__ \ | (_| | || (_) | |   \n   |_____|_____/ \____/ \__|_|  \__,_|_| |_|___/_|\__,_|\__\___/|_|   \n                  -ISO999:2016 PDF to JSON translator-                    \n\n\n")

    document_as_string = rectify_document_as_string(encode_bytes(analyze_pdf("/home/fabian/Documents/repositories/adam_system/adam4/UNE-EN_ISO_9999=2017.pdf")))
    superhaystack = generate_superhaystack(document_as_string , verbose=True)
    # item = get_next_item(superhaystack , True)
    # superhaystack = delete_next_item(superhaystack , item)
    # item = get_next_item(superhaystack, True)
    # superhaystack = delete_next_item(superhaystack, item)
    # item = get_next_item(superhaystack, True)
    # superhaystack = delete_next_item(superhaystack, item)
    # item = get_next_item(superhaystack, True)
    # superhaystack = delete_next_item(superhaystack, item)
    # item = get_next_item(superhaystack, True)
    # superhaystack = delete_next_item(superhaystack, item)
    # item = get_next_item(superhaystack, True)
    # superhaystack = delete_next_item(superhaystack, item)


if __name__ == "__main__":
    main()