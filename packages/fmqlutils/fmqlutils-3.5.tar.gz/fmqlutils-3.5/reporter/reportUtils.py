#!/usr/bin/env python
# -*- coding: utf8 -*-

# (c) 2015-2020 caregraf

import re
import math
import textwrap

"""
TODO: consider combining into a report maker set ie/ make table (accept sets of rows too) and
make doc, add table, add graphic ref, add text, open section ...

Ala https://datapane.com/
"""
    
# #################### Markdown Utilities ###################

class MarkdownTable:

    """
    Supports:
    - first column # or not
    - explicit formatting by adding :'s to cols. Name "COL" given as :COL: is center aligned, :COL, left aligned, COL:, right aligned. Default is centered (:---:)
    - count of rows (for intro blurbs)
    """
    def __init__(self, cols, includeNo=True, defaultColMarker=":---:"):
        self.__noCols = len(cols)
        self.__includeNo = includeNo
        self.__rowNo = 0
        colNames = []
        colMarkers = []
        if includeNo:
            colNames.append("\#")
            colMarkers.append(":---:")
        for col in cols:
            formattedMatch = re.match(r'(:?)([^\:]+)(:?)$', col)
            if not formattedMatch: # may have :: or : inside etc => doesn't want format
                colNames.append(col)
                colMarkers.append(defaultColMarker)
                continue
            colNames.append(formattedMatch.group(2))
            if formattedMatch.group(1) == "" and formattedMatch.group(3) == "":
                colMarkers.append(defaultColMarker)
                continue
            colMarkers.append("{}---{}".format(formattedMatch.group(1), formattedMatch.group(3)))
        self.__tmu = " | ".join(colNames) + "\n" + " | ".join(colMarkers) + "\n"

    def addRow(self, vals):
        if len(vals) < self.__noCols:
            raise Exception("Need values for all cols")
        self.__rowNo += 1
        if self.__includeNo:
            rmu = "{}".format(str(self.__rowNo))
        else:
            rmu = ""
        for val in vals:
            if rmu:
                rmu += " | "
            if val == "":
                rmu += "&nbsp;"
            else:
                if isinstance(val, int):
                    rmu += format(val, ",")
                elif isinstance(val, list):
                    if len(val) != 2:
                        raise Exception("Use 2 piece list for url")
                    rmu += "[{}]({})".format(val[0], val[1])
                else:
                    rmu += str(val)
        rmu += "\n"
        self.__tmu += rmu

    def addSeparatorRow(self):
        rmu = " | ".join(["&nbsp;"] * (self.__noCols + (1 if self.__includeNo else 0))) + "\n"
        self.__tmu += rmu

    def md(self):
        return self.__tmu
        
    def rowCount(self):
        return self.__rowNo

"""
One line version
"""
def mdTable(rows, headers, count=False):
    """
    mdTable([["X", "Y"], [1]], ["X", "Y"])
    
    Decision NOT to force column values to be strings. Better to 
    format outside here (using escapeString etc) as approach differs
    with nature of data.
    """    
    noColumns = max(len(row) for row in rows)
    if len(headers) != noColumns:
        raise Exception("Expect headers to cover number of columns in all rows")
    if count:
        headers.insert(0, "\#")
    md = "\n" # ensure gap before
    # pad rows
    for i, row in enumerate(rows, 1):
        if len(row) < noColumns:
            for padNo in range(noColumns - len(row)):
                row.append("")
        if count:
            row.insert(0, str(i))
        if sum(1 for member in row if not isinstance(member, str)):
            raise Exception("Passed in a value that isn't a string")
    md += " | ".join(headers) + "\n"
    md += "|".join(["---" for i in range(len(headers))]) + "\n" 
    for i, row in enumerate(rows, 1):
        md += " | ".join(row) + "\n"
    return md
    
def mdHeaderRef(label):
    """
    Form: "#" with - in lowercase used by github for
    id's for headers. Use when want to refer to an anchor
    in a table of contents
    
    ex/ [" + label + "](#" + mdHeaderRef(label) + ")
    """
    return re.sub(' ', '-', label).lower()
  
def mdEscapeString(text, maxLen=-1):
    """
    - Using HTML entities to ensure no markdown interpretation of regexp or transforms
    - putting in ZERO WIDTH SPACE to tell browser when to split lines
      - removing \r first as deciding on new split (and \r will mess up MD
    """
    ESCAPES = {
        "(": "&#40;",
        ")": "&#41;",
        "[": "&#91;",
        "]": "&#93;",
        "?": "&#63;",
        "$": "&#38;",
        "<": "&#60;",
        ">": "&#62;",
        "^": "&#94;",
        "\\": "&#92;",
        "$": "&#36;",
        "|": "&#124;",
        "_": "&#95;"
    }
    
    text = re.sub(r'\r', ' ', text) # if embedded \r's get rid of them
    
    if maxLen != -1:
        text = "\r".join(textwrap.wrap(text, maxLen))
    #    # text = "\r".join([text[i:i+maxLen] for i in range(0, len(text), maxLen)])
    text = "".join(ESCAPES.get(c,c) for c in text)
    if maxLen != -1:
        text = re.sub(r'\r', "&#8203;", text)
    
    return text
    
# ################################## Sizing Utilities #######################

def convertSize(size):
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size,1024)))
   p = math.pow(1024,i)
   s = round(size/p,2)
   if (s > 0):
       return '%s %s' % (s,size_name[i])
   else:
       return '0B'

# see: http://goo.gl/kTQMs
SYMBOLS = {
    'customary'     : ('B', 'KB', 'MB', 'GB', 'T', 'P', 'E', 'Z', 'Y'),
    # 'customary'     : ('B', 'K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y'),
    'customary_ext' : ('byte', 'kilo', 'mega', 'giga', 'tera', 'peta', 'exa',
                       'zetta', 'iotta'),
    'iec'           : ('Bi', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi', 'Yi'),
    'iec_ext'       : ('byte', 'kibi', 'mebi', 'gibi', 'tebi', 'pebi', 'exbi',
                       'zebi', 'yobi'),
}    

def human2bytes(s):
    """
    Attempts to guess the string format based on default symbols
    set and return the corresponding bytes as an integer.
    When unable to recognize the format ValueError is raised.

      >>> human2bytes('0 B')
      0
      >>> human2bytes('1 K')
      1024
      >>> human2bytes('1 M')
      1048576
      >>> human2bytes('1 Gi')
      1073741824
      >>> human2bytes('1 tera')
      1099511627776

      >>> human2bytes('0.5kilo')
      512
      >>> human2bytes('0.1  byte')
      0
      >>> human2bytes('1 k')  # k is an alias for K
      1024
      >>> human2bytes('12 foo')
      Traceback (most recent call last):
          ...
      ValueError: can't interpret '12 foo'
    """
    init = s
    num = ""
    while s and s[0:1].isdigit() or s[0:1] == '.':
        num += s[0]
        s = s[1:]
    num = float(num)
    letter = s.strip()
    for name, sset in SYMBOLS.items():
        if letter in sset:
            break
    else:
        if letter == 'k':
            # treat 'k' as an alias for 'K' as per: http://goo.gl/kTQMs
            sset = SYMBOLS['customary']
            letter = letter.upper()
        else:
            raise ValueError("can't interpret %r" % init)
    prefix = {sset[0]:1}
    for i, s in enumerate(sset[1:]):
        prefix[s] = 1 << (i+1)*10
    return int(num * prefix[letter])

# ##################### MUBVC ####################

"""
Note: forceShowCount is to allow an ST BVC use to force a count for
a single value if count < total
"""
def muBVC(bvc, separator=", ", forceShowCount=False, countOnlyIfOver=-1, totalOver=-1):
    def labelKey(k):
        if re.search(r' \[', k):
            return k.split(" [")[0]
        if not re.search(r':', k):
            return k
        return k.split(":")[1]
    if len(bvc) == 1:
        k = list(bvc)[0]
        if not forceShowCount:
            return labelKey(k)
        return "{} [{:,}]".format(labelKey(k), bvc[k])
    if countOnlyIfOver != -1 and len(bvc) > countOnlyIfOver:
        return "{:,}".format(len(bvc))
    if totalOver != -1 and len(bvc) > totalOver:
        sBVs = sorted(list(bvc), key=lambda x: bvc[x], reverse=True)
        return "{} and {:,} Others [{:,}]".format(
            separator.join(["{} [{:,}]".format(labelKey(k), bvc[k]) for k in sBVs[0:totalOver]]),
            len(sBVs[totalOver:]),
            sum(bvc[k] for k in sBVs[totalOver:])
        )
    mu = separator.join(["{} [{:,}]".format(labelKey(k), bvc[k]) for k in sorted(bvc, key=lambda x: bvc[x], reverse=True)])
    return mu
    
# ###################### Simple % stuff for text reports #########

# TODO: change to muX

def reportAbsAndPercent(abs, total):
    perc = reportPercent(abs, total) 
    if perc != "0.0%":
        return "{:,}".format(abs) + " (" + perc + ")"
    return "{:,}".format(abs)

def reportPercent(piece, total, dashIfZero=False):
    if not total: # can't divide by 0
        return "0.0%" if dashIfZero == False else "-"
    return str(makePercent(piece, total)) + "%"

def makePercent(piece, total):
    return round((float(piece) * 100)/float(total), 2)
    
# ######################### Tests and Demos #########################

def main():
    
    open("dump.md", "w").write(mdTable([["X", "(Y)"], [1], ["jessy went to the farm with mary to pick hay", "and pick up some stones and build a castle and call out to the birds before grabbing an egg and devouring it raw"]], ["X", "Y"]))
    
if __name__ == "__main__":
    main()
